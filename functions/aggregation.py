#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function to aggregate incidents spatially to
CTUs and temporally by CTU/week combinations.

Alters/updates values in ctu_accidents & time_series tables.

@Author: Luke Zaruba
@Date: Aug 31, 2023
@Version: 0.0.0
"""

import os

import functions_framework
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()


def update_city_id(db):
    with db.connect() as connection:
        city_icr_query = """
        SELECT ctu.id, acc.icr
        FROM ctu
        JOIN geo_accidents acc
        ON ST_Intersects(ctu.geom, acc.geom)
        WHERE acc.city_id IS NULL;
        """

        accident_cities_result = connection.execute(text(city_icr_query))
        accident_cities = accident_cities_result.fetchall()

        # UPDATE CITY ID VALUES
        for accident in accident_cities:
            update_query = f"""
            UPDATE geo_accidents
            SET city_id = {int(accident[0])}
            WHERE icr = {int(accident[1])}
            """

            connection.execute(text(update_query))
            connection.commit()


def geocoding_qaqc_table(db):
    with db.connect() as connection:
        # CREATE COPY OF geo_accidents W/O INVALID GC RECORDS
        drop_query = "DROP TABLE IF EXISTS geo_accidents_mn"
        connection.execute(text(drop_query))
        connection.commit()

        copy_query = """
        CREATE TABLE IF NOT EXISTS geo_accidents_mn AS
        SELECT acc.*
        FROM geo_accidents acc
        JOIN ctu
        ON ST_Intersects(ctu.geom, acc.geom)
        """

        connection.execute(text(copy_query))
        connection.commit()


def update_ctu_incident_counts(db):
    with db.connect() as connection:
        # QUERY TO GET COUNTS FOR EACH CTU
        count_city_icr_query = """
        SELECT ctu.id, COUNT(acc.geom)::int AS total_incident_count
        FROM ctu
        JOIN geo_accidents acc
        ON ST_Contains(ctu.geom, acc.geom)
        GROUP BY ctu.id
        """

        acc_ct_cities_result = connection.execute(text(count_city_icr_query))
        acc_ct_cities = acc_ct_cities_result.fetchall()

        # UPDATE CITY ID VALUES
        for city in acc_ct_cities:
            update_query = f"""
            UPDATE ctu_accidents
            SET total_incident_count = {int(city[1])}
            WHERE id = {int(city[0])}
            """

            connection.execute(text(update_query))
            connection.commit()


def global_time_series(db):
    with db.connect() as connection:
        # DROP EXISTING TABLE
        drop_query = "DROP TABLE IF EXISTS glb_wk_time_series"
        connection.execute(text(drop_query))
        connection.commit()

        create_query = """
        CREATE TABLE IF NOT EXISTS glb_wk_time_series AS
        SELECT COUNT(*) AS incident_count,
        date_trunc('week', incident_date)::date AS week
        FROM geo_accidents
        WHERE date_trunc('week', incident_date)::date > '2016-12-31'
        GROUP BY date_trunc('week', incident_date)::date
        """

        connection.execute(text(create_query))
        connection.commit()


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

    update_city_id(db)

    update_ctu_incident_counts(db)

    geocoding_qaqc_table(db)

    global_time_series(db)


if __name__ == "__main__":
    main()
