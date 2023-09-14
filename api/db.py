#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database handling for RESTful API

@Author: Luke Zaruba
@Date: Sep 14, 2023
@Version: 0.0.0
"""

from __future__ import annotations

import os

import psycopg2


class Database:
    def __init__(
        self, host: str, user: str, password: str, db_name: str, port: int
    ) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = port

        # Set Connection to None
        self.connection = None

    @classmethod
    def initialize_from_env(cls) -> Database:
        # Extract Secrets
        host = os.environ.get("DB_HOST")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        db_name = os.environ.get("DB_NAME")
        port = os.environ.get("DB_PORT")

        # Return Instance
        return cls(host, user, password, db_name, port)

    def connect(self) -> None:
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.db_name,
            user=self.user,
            password=self.password,
            port=self.port,
        )

    def query(self, query: str) -> str:
        # Open Cursor
        with self.connection.cursor() as c:
            # Try to Execute
            try:
                # Execute Query
                c.execute(query)

                # Commit to DB
                self.connection.commit()

                # Return Output
                return c.fetchall()

            except Exception as e:
                # Roll Back Transaction if Invalid Query
                self.connection.rollback()

                # Display Error
                return "Error: " + str(e)

    def close(self):
        # Close Connection
        self.connection.close()

        # Set Connection to None
        self.connection = None


class Query:
    """
    A class used to store SQL queries.
    """

    # Incident Queries
    INCIDENT_GEOJSON = """
    SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(ST_AsGeoJSON(gam.*)::json))
    FROM geo_accidents_mn gam;
    """

    # INCIDENT_ICR = """
    # SELECT json_agg(ST_AsGeoJSON(gam.*)::json))
    # FROM geo_accidents_mn gam
    # WHERE gam.icr == %s;
    # """

    INCIDENT_TOTAL = """
    SELECT COUNT(icr)
    FROM raw_accidents;
    """

    INCIDENT_LAST_WEEK = """
    SELECT incident_count
    FROM glb_wk_time_series
    ORDER BY week DESC
    LIMIT(1);
    """

    INCIDENT_CURRENT_CLUSTERS = """
    SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(ST_AsGeoJSON(ccf.*)::json))
    FROM crnt_clstr_ftprnt ccf;
    """

    INCIDENT_YEARLY_CLUSTERS = """
    SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(ST_AsGeoJSON(ctf.*)::json))
    FROM clstr_ts_ftprnt ctf;
    """

    INCIDENT_CLUSTER_STABILITY = """
    SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(ST_AsGeoJSON(cuf.*)::json))
    FROM clstr_union_ftprnt cuf;
    """

    # CTU Queries
    CTU_GEOJSON = """
    SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(ST_AsGeoJSON(ctu.*)::json))
    FROM ctu_accidents ctu;
    """

    # Metrics Queries
    METRICS_TIMESERIES = """
    SELECT *
    FROM glb_wk_time_series
    ORDER BY week;
    """

    METRICS_ALCOHOL = """
    SELECT alcohol, COUNT(alcohol)
    FROM raw_people
    GROUP BY alcohol
    ORDER BY COUNT(alcohol);
    """

    METRICS_SEATBELT = """
    SELECT seatbelt, COUNT(seatbelt)
    FROM raw_people
    GROUP BY seatbelt
    ORDER BY COUNT(seatbelt);
    """

    METRICS_HELMET = """
    SELECT helmet, COUNT(helmet)
    FROM raw_people
    GROUP BY helmet
    ORDER BY COUNT(helmet);
    """

    METRICS_CONDITION = """
    SELECT road_condition, COUNT(road_condition)
    FROM raw_accidents
    WHERE road_condition <> ''
    GROUP BY road_condition
    ORDER BY COUNT(road_condition);
    """

    METRICS_TYPE = """
    SELECT incident_type, COUNT(incident_type)
    FROM raw_accidents
    GROUP BY incident_type;
    """

    METRICS_VEHICLE_COUNT = """
    SELECT vehicles_involved, COUNT(vehicles_involved)
    FROM raw_accidents
    WHERE vehicles_involved < 100
    GROUP BY vehicles_involved
    ORDER BY vehicles_involved;
    """
