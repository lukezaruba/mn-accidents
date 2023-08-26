from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)


@app.route("/points/geojson")
def get_points_geojson():
    try:
        # Fine to leave localhost creds
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            database="mnaccidents",
        )
        cursor = conn.cursor()

        cursor.execute(
            "SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(ST_AsGeoJSON(tbl.*)::json)) FROM geo_accidents AS tbl"
        )
        row = cursor.fetchone()
        json_result = row[0]

        cursor.close()
        conn.close()

        return jsonify(json_result)

    except (Exception, psycopg2.Error) as error:
        print("Error retrieving points:", error)
        return jsonify({"error": "Failed to retrieve points"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
