#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function to aggregate incidents spatially to
CTUs and temporally by CTU/week combinations.

Alters/updates values in ctu_accidents & time_series tables.

@Author: Luke Zaruba
@Date: Aug 16, 2023
@Version: 0.0.0
"""

import json
import os

import functions_framework
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def update_city_id(db):
    query = """
    SELECT ctu.id, acc.icr
    FROM ctu
    JOIN geo_accidents acc
    ON ST_Intersects(ctu.geom, acc.geom)
    """

    with db.connect() as connection:
        accident_cities_result = connection.execute(text(query))
        accident_cities = accident_cities_result.fetchall()

        # DROP INVALID GEOCODED RECORDS
        valid_icrs = [int(i[1]) for i in accident_cities]

        drop_query = f"""
        DROP FROM geo_accidents
        WHERE icr NOT IN
        {tuple(valid_icrs)}
        """

        connection.execute(text(drop_query))
        connection.commit()

        # UPDATE CITY ID VALUES
        for accident in accident_cities:
            update_query = f"""
            UPDATE TABLE geo_accidents
            SET city_id = {int(accident[0])}
            WHERE icr = {int(accident[1])}
            """

            connection.execute(text(update_query))
            connection.commit()


def rebuild_spatial_index(db):
    ...
    # INDEX
    # CREATE INDEX nyc_census_blocks_geom_idx
    #     ON nyc_census_blocks
    #     USING GIST (geom);


def replace_time_series_table(db):
    ...
    # TIME SERIES TABLE CREATION
    # DROP TABLE time_series IF EXISTS;
    # CREATE TABLE time_series AS (
    #     WITH all_combinations AS (
    #         SELECT
    #             ctu.id,
    #             generate_series(
    #                 min(ga.incident_date)::date,
    #                 max(ga.incident_date)::date,
    #                 '1 week'::interval
    #             )::date AS week
    #         FROM ctu
    #         CROSS JOIN geo_accidents ga
    #         GROUP BY ctu.id
    #     )
    #     SELECT ac.id, ac.week, COALESCE(COUNT(ga.incident_date), 0) AS record_count
    #     FROM all_combinations ac
    #     LEFT JOIN geo_accidents ga ON ac.id = ga.city_id AND ac.week = date_trunc('week', ga.incident_date)::date
    #     GROUP BY ac.id, ac.week
    #     ORDER BY ac.id, ac.week;
    # )


def update_ctu_incident_counts(db):
    ...
    # QUERY TO GET COUNTS FOR EACH CTU
    query = """
    SELECT ctu.id, COUNT(acc.geom)::int AS incident_ct
    FROM ctu
    JOIN geo_accidents acc
    ON ST_Contains(ctu.geom, acc.geom)
    GROUP BY ctu.id
    """


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

    update_city_id(db)

    replace_time_series_table(db)

    rebuild_spatial_index(db)
