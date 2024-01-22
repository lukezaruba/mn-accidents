#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function to perform LISA & ADBSCAN
analyses on accident data.


@Author: Luke Zaruba
@Date: Aug 31, 2023
@Version: 0.0.0
"""

import os

import functions_framework
import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from dotenv import load_dotenv
from esda.adbscan import ADBSCAN, get_cluster_boundary, remap_lbls
from pysal.explore import esda
from pysal.lib import weights
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()


def run_lisa(db):
    # Read in Polygon Data
    ctu_gdf = gpd.read_postgis("SELECT * FROM ctu_accidents", db)

    # Standardize Incident Count by Total Road Length
    ctu_gdf["total_road_length"] = ctu_gdf["total_road_length"].replace(0, 1)
    ctu_gdf["rd_stdrd_incidents"] = (
        ctu_gdf["total_incident_count"] / ctu_gdf["total_road_length"]
    )

    # Set up LISA
    data = ctu_gdf["rd_stdrd_incidents"].values

    w = weights.Queen.from_dataframe(ctu_gdf)

    # Perform Local Moran's I analysis
    moran_loc = esda.Moran_Local(data, w)

    # Add the resulting values to the GDF
    ctu_gdf["lmi_i"] = moran_loc.Is
    ctu_gdf["lmi_p"] = moran_loc.p_sim
    ctu_gdf["lmi_sig"] = 1 * (moran_loc.p_sim < 0.05)
    ctu_gdf["lmi_q"] = moran_loc.q

    # Add the labels to the GDF
    labels = {
        0: "NS",
        1: "HH",
        2: "LH",
        3: "LL",
        4: "HL",
    }

    ctu_gdf["lmi_label"] = pd.Series(
        moran_loc.q * (1 * (moran_loc.p_sim < 0.05)), index=ctu_gdf.index
    ).map(labels)

    # Update Database
    update_columns = ctu_gdf[["id", "lmi_i", "lmi_p", "lmi_sig", "lmi_q", "lmi_label"]]

    updates = list(update_columns.itertuples(index=False, name=None))

    with db.connect() as connection:
        # UPDATE CTU VALUES
        for ctu in updates:
            update_query = f"""
            UPDATE ctu_accidents
            SET lmi_i = {ctu[1]},
            lmi_p = {ctu[2]},
            lmi_sig = {ctu[3]},
            lmi_q = {ctu[4]},
            lmi_label = '{ctu[5]}'
            WHERE id = {ctu[0]}
            """

            connection.execute(text(update_query))
            connection.commit()


def run_monthly_adbscan(db):
    # Read in Incident Data
    incidents_gdf = gpd.read_postgis("SELECT * FROM geo_accidents_mn", db)

    incidents_gdf["X"] = incidents_gdf.geometry.x
    incidents_gdf["Y"] = incidents_gdf.geometry.y

    incidents_gdf["year"] = (
        incidents_gdf["incident_date"].dt.to_period("Y").astype(str).astype(int)
    )

    # Monthly ADBSCAN
    df_list = []

    for timestep in incidents_gdf.year.unique():
        year_df = incidents_gdf.loc[(incidents_gdf["year"] == timestep)].copy()

        yr_adbs = ADBSCAN(
            0.15, year_df.shape[0] * 0.01, pct_exact=0.5, reps=50, keep_solus=True
        )
        yr_adbs.fit(year_df)

        yr_polys = get_cluster_boundary(yr_adbs.votes["lbls"], year_df, crs=year_df.crs)

        data = {"year": timestep, "geometry": yr_polys}

        footprint_gdf = gpd.GeoDataFrame(data)

        df_list.append(footprint_gdf)

    yearly_footprints = pd.concat(df_list)

    # Simplify Yearly Footprints
    yearly_footprints_simplified = gpd.GeoDataFrame(
        {
            "geometry": yearly_footprints.buffer(10, join_style=1).buffer(
                -10, join_style=1
            )
        }
    )

    # Calculate Stability w/ Interset/Union
    union_df = _count_overlapping_features(yearly_footprints_simplified)

    # Upload Union to DB
    union_df.columns = ["cluster_id", "stability_count", "geom"]

    union_df = union_df.set_geometry("geom")

    union_df.to_postgis("clstr_union_ftprnt", db, if_exists="replace")

    # Upload TS to DB
    yearly_footprints.insert(0, "cluster_id", range(0, len(yearly_footprints)))
    yearly_footprints.columns = ["cluster_id", "cluster_year", "geom"]

    yearly_footprints = yearly_footprints.set_geometry("geom")

    yearly_footprints.to_postgis("clstr_ts_ftprnt", db, if_exists="replace")


def run_total_adbscan(db):
    # Read in Incident Data
    incidents_gdf = gpd.read_postgis("SELECT * FROM geo_accidents_mn", db)

    incidents_gdf["X"] = incidents_gdf.geometry.x
    incidents_gdf["Y"] = incidents_gdf.geometry.y

    # Get clusters
    adbs = ADBSCAN(
        0.15, incidents_gdf.shape[0] * 0.01, pct_exact=0.5, reps=50, keep_solus=True
    )
    adbs.fit(incidents_gdf)

    # Get Footprints
    polys = get_cluster_boundary(
        adbs.votes["lbls"], incidents_gdf, crs=incidents_gdf.crs
    )

    data = {"geom": polys}

    footprint_gdf = gpd.GeoDataFrame(data)

    # Upload to Postgres
    footprint_gdf.insert(0, "cluster_id", range(0, len(footprint_gdf)))

    footprint_gdf.columns = ["cluster_id", "geom"]

    footprint_gdf = footprint_gdf.set_geometry("geom")

    footprint_gdf.to_postgis("crnt_clstr_ftprnt", db, if_exists="replace")


def _count_overlapping_features(in_gdf):
    # CREDS: https://gis.stackexchange.com/questions/387773/count-overlapping-features-using-geopandas
    # Get the name of the column containing the geometries
    geom_col = in_gdf.geometry.name

    # Setting up a single piece that will be split later
    input_parts = [in_gdf.unary_union.buffer(0)]

    # Finding all the "cutting" boundaries. Note: if the input GDF has
    # MultiPolygons, it will treat each of the geometry's parts as individual
    # pieces.
    cutting_boundaries = []
    for i, row in in_gdf.iterrows():
        this_row_geom = row[geom_col]
        this_row_boundary = this_row_geom.boundary
        if this_row_boundary.geom_type[: len("multi")].lower() == "multi":
            cutting_boundaries = cutting_boundaries + list(this_row_boundary.geoms)
        else:
            cutting_boundaries.append(this_row_boundary)

    # Split the big input geometry using each and every cutting boundary
    for boundary in cutting_boundaries:
        splitting_results = []
        for j, part in enumerate(input_parts):
            new_parts = list(shapely.ops.split(part, boundary).geoms)
            splitting_results = splitting_results + new_parts
        input_parts = splitting_results

    # After generating all of the split pieces, create a new GeoDataFrame
    new_gdf = gpd.GeoDataFrame(
        {
            "id": range(len(splitting_results)),
            geom_col: splitting_results,
        },
        crs=in_gdf.crs,
        geometry=geom_col,
    )

    # Find the new centroids.
    new_gdf["geom_centroid"] = new_gdf.centroid

    # Starting the count at zero
    new_gdf["count_intersections"] = 0

    # For each of the `new_gdf`'s rows, find how many overlapping features
    # there are from the input GDF.
    for i, row in new_gdf.iterrows():
        new_gdf.loc[i, "count_intersections"] = (
            in_gdf.intersects(row["geom_centroid"]).astype(int).sum()
        )
        pass

    # Dropping the column containing the centroids
    new_gdf = new_gdf.drop(columns=["geom_centroid"])[
        ["id", "count_intersections", geom_col]
    ]

    return new_gdf


@functions_framework.http
def main():
    # Creating Database Engine Instance
    _db_url = URL.create(
        drivername="postgresql",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_NAME"],
    )
    db = create_engine(_db_url)

    # LISA
    run_lisa(db)

    # ADBSCAN
    run_total_adbscan(db)

    run_monthly_adbscan(db)


if __name__ == "__main__":
    main()
