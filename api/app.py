#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RESTful API

@Author: Luke Zaruba
@Date: Sep 14, 2023
@Version: 0.0.0
"""

import os

from flask import Flask, jsonify
from flask_restx import Api, Namespace, Resource

from db import Database, Query

# Set up DB Connection
db = Database.initialize_from_env()

# Configure API
app = Flask(__name__)
api = Api(
    app,
    prefix="/api/v1",
    doc="/api/v1/doc",
    version="1.0",
    title="Minnesota Crash Analysis API",
    description="A RESTful API used for accessing geospatial data related to vehicle crash data in Minnesota.",
)

# Create Namespaces
incidents_namespace = Namespace(
    "incidents",
    description="Operations for accessing incident data",
)

ctu_namespace = Namespace(
    "ctu",
    description="Operations for accessing CTU data",
)

metrics_namespace = Namespace(
    "metrics",
    description="Operations for accessing crash metrics",
)

# Add Namespaces to API
api.add_namespace(incidents_namespace)
api.add_namespace(ctu_namespace)
api.add_namespace(metrics_namespace)


# Routes for Incidents Namespace
@incidents_namespace.route(
    "/geojson",
)
class Incidents(Resource):
    @incidents_namespace.doc(
        description="Retrieves the incident locations and attributes for all incidents."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.INCIDENT_GEOJSON)[0][0]
        db.close()

        # Return
        return out


@incidents_namespace.route(
    "/total",
)
class IncidentTotal(Resource):
    @incidents_namespace.doc(
        description="Retrieves the total number of incidents all-time."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.INCIDENT_TOTAL)[0][0]
        db.close()

        # Return
        return out


@incidents_namespace.route(
    "/last-week",
)
class IncidentsLastWeek(Resource):
    @incidents_namespace.doc(
        description="Retrieves the number of incidents in the past week."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.INCIDENT_LAST_WEEK)[0][0]
        db.close()

        # Return
        return out


@incidents_namespace.route(
    "/crnt-clstr-ftprnt",
)
class CurrentClusters(Resource):
    @incidents_namespace.doc(
        description="Retrieves footprints based on current all-time clustering analysis."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.INCIDENT_CURRENT_CLUSTERS)[0][0]
        db.close()

        # Return
        return out


@incidents_namespace.route(
    "/yrly-clstr-ftprnt",
)
class YearlyClusters(Resource):
    @incidents_namespace.doc(
        description="Retrieves footprints for each year of the analysis."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.INCIDENT_YEARLY_CLUSTERS)[0][0]
        db.close()

        # Return
        return out


@incidents_namespace.route(
    "/clstr-ftprnt-stblty",
)
class ClusterStability(Resource):
    @incidents_namespace.doc(
        description="Retrieves footprints from the cluster stability analysis."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.INCIDENT_CLUSTER_STABILITY)[0][0]
        db.close()

        # Return
        return out


# Routes for CTU Namespace
@ctu_namespace.route(
    "/geojson",
)
class CTUs(Resource):
    @ctu_namespace.doc(
        description="Retrieves city, township, and unorganized territory boundaries and analysis results."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.CTU_GEOJSON)[0][0]
        db.close()

        # Return
        return out


# Routes for Metrics Namespace
@metrics_namespace.route(
    "/alcohol",
)
class Alcohol(Resource):
    @metrics_namespace.doc(
        description="Retrieves the number of drivers based on whether alcohol was present or not."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.METRICS_ALCOHOL)
        db.close()

        # Return
        return jsonify(out)


@metrics_namespace.route(
    "/seatbelt",
)
class Seatbelt(Resource):
    @metrics_namespace.doc(
        description="Retrieves the number of people based on whether seatbelts were used or not."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.METRICS_SEATBELT)
        db.close()

        # Return
        return jsonify(out)


@metrics_namespace.route(
    "/helmet",
)
class Helmet(Resource):
    @metrics_namespace.doc(
        description="Retrieves the number of people based on whether helmets were used or not."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.METRICS_HELMET)
        db.close()

        # Return
        return jsonify(out)


@metrics_namespace.route(
    "/condition",
)
class Condition(Resource):
    @metrics_namespace.doc(
        description="Retrieves the number of incidents based on the road conditions."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.METRICS_CONDITION)
        db.close()

        # Return
        return jsonify(out)


@metrics_namespace.route(
    "/accident-type",
)
class AccidentType(Resource):
    @metrics_namespace.doc(
        description="Retrieves the number of incidents based on the type of incident."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.METRICS_TYPE)
        db.close()

        # Return
        return jsonify(out)


@metrics_namespace.route(
    "/timeseries",
)
class TimeSeries(Resource):
    @metrics_namespace.doc(
        description="Retrieves the time series of incidents for each week."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.METRICS_TIMESERIES)
        db.close()

        # Return
        return jsonify(out)


@metrics_namespace.route(
    "/vehicle-count",
)
class VehicleCount(Resource):
    @metrics_namespace.doc(
        description="Retrieves the number of incidents based on the number of vehicles involved."
    )
    def get(self):
        # Query
        db.connect()
        out = db.query(Query.METRICS_VEHICLE_COUNT)
        db.close()

        # Return
        return jsonify(out)


if __name__ == "__main__":
    # Development
    # app.run(debug=True)

    # Production
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
