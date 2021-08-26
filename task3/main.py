# Task3

# Need to do
# have the endpoint provide a query string to allow selection of a time period.
# The JSON object is not being formatted correctly on the return. It is adding in escaping \
# is restpoint technically RESTful?
# Sinepct the data coming back. Is it actually an average or just being smooshed together.
# How to group the data into 5 minute averages?

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sys

import flask
import numpy as np
import sqlite3
import json
import requests
import pandas as pd

from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)


# API Functions
class HelloWorld(Resource):
    def get(self):
        result = query_db_values('2021-08-26T12:00:00', '2021-08-26T12:15:00', DATABASE)
        print(result)
        return jsonify(result)

api.add_resource(HelloWorld, '/')
# Get the SWPC data and return it as JSON.
def get_swpc_json(noaa_url):
    print("Attempting to retrieve SWPC data from NOAA ...")
    try:
        swpc_data = requests.get(noaa_url)
    except Exception as E:
        print("Failed to connect", E)
    print("Data successfully received.")
    return swpc_data.json()


# Create an SQLite3 DB from JSON data.
# If db already exists, remove it and recreate to ensure fresh data.
def create_swpc_db(db, swpc_json_data):
    # Check if db exists and delete it.
    try:
        if os.path.isfile(db):
            print("Deleting old db:", db)
            os.remove(db)
    except Exception as E:
        print("Failed to delete old database:", db, E)
        sys.exit(1)

    # Convert JSON to DB.
    # Pandas handles the transform of JSON to SQL.
    try:
        df = pd.DataFrame(swpc_json_data)
        print("Creating and populating new", db)
        conn = sqlite3.connect(db)
        df.to_sql("swpcdata", conn)
        conn.commit()
    except ValueError:
        print("Invalid JSON data received. Cannot convert to DB. Aborting.")
        sys.exit(1)
    except Exception as E:
        print("Failed to connect", E.__class__.__name__)
        sys.exit(1)
    finally:
        # Close DB connection.
        conn.close()


# Query values from the db between the start and end times.
# The maximum query range is 1 hour
def query_db_values(start_time, end_time, db):
    # The average time/number of readings
        AVERAGE_TIME=5
    # The number of sources
        NUM_OF_SOURCES=2
    # try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM swpcdata WHERE time_tag >= ? AND time_tag <= ?', (start_time, end_time))
        # data_between_times = cur.fetchall()

        # Get the headers to build a JSON object
        row_headers = [header[0] for header in cur.description]  # this will extract row headers
        data_between_times = []
        for row in cur.fetchall():
            data_between_times.append(dict(zip(row_headers, row)))

        # Calculate average of 5 minutes
        df = pd.read_json(json.dumps(data_between_times))
        avereged_swpc_json = df.groupby(np.arange(len(df)) // (AVERAGE_TIME*NUM_OF_SOURCES)).mean().to_json()
        print(avereged_swpc_json)
        return avereged_swpc_json

        # print(df)
    # except Exception as E:
    #     print("Error", E)



if __name__ == '__main__':
    NOAA_URL = 'https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json'
    DATABASE = 'swpc.db'

    # app = Flask(__name__)
    # @app.route("/")
    # def hello_world():
    #     return "<p>Hello, World!</p>"

    # Get SWPC data
    swpc_json_data = get_swpc_json(NOAA_URL)
    # Create SQLite3 table from JSON data
    create_swpc_db(DATABASE, swpc_json_data)

    query_db_values('2021-08-26T12:00:00', '2021-08-26T12:15:00', DATABASE)

    app.run(debug=True)
