# Task3 - An API endpoint for querying SWPC data from noaa between two times.
# Live datetime SWPC JSON data is downloaded from https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json.
# The JSON data is resampled to provide averages in five minute blocks (12:00, 12:05, 12:10, ...) and stored in a SQLIte DB.
# An API endpoint is created on localhost:5000 to allow the data to be queried and returned in JSON format.
# The request window is a maximum of on hour.

# Testing instructions
# Install the Python dependencies defined in requirements.txt
# Run the application/webserver with `python task3.ty'
# Using a browser or curl/wget query the endpoint such as:
#   http://127.0.0.1:5000/spwcdata/start_datetime/end_datetime
# Replace the start and end datetime with a current/valid datetime and ensure the format "%Y-%m-%dT%H:%M:%S"
# For example:
#   http://127.0.0.1:5000/spwcdata/2021-08-27T11:30:00/2021-08-27T12:15:00
# The queried data should be returned in valid, pretty printed JSON format.


import os
import sys
import sqlite3
import pandas
import requests
import pandas as pd

from flask import Flask
from flask_restful import abort, Api, Resource

# Define Flask default app
app = Flask(__name__)
api = Api(app)

# Constants
NOAA_URL = 'https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json'
DATABASE = 'swpc.db'
MAX_TIME_SPAN_SECONDS = 3600


# Endpoint to return averaged (5min) data between start and end datetime.
class SwpcAPI(Resource):
    def get(self, start_date_time, end_date_time):
        # Ensure correct DatTime Format "%Y-%m-%dT%H:%M:%S" to convert to our db format "%Y-%m-%d %H:%M:%S"
        start_time = pandas.to_datetime(start_date_time)
        end_time = pandas.to_datetime(end_date_time)

        # Check end time is after start time
        if start_time > end_time:
            abort(400, message="Invalid time request range. "
                               "The end date is after the start and the format is %Y-%m-%dT%H:%M:%S")
        # Max time span of 60 minutes (3600 seconds)
        if (end_time - start_time).total_seconds() > MAX_TIME_SPAN_SECONDS:
            abort(400, message="Invalid time request range. Ensure request is less then 1 hour.")

        try:
            # Convert to required format
            converted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
            converted_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as E:
            print("Invalid API request", E)
            abort(400, message="Error in request please ensure time format is start_time/end_time %Y-%m-%dT%H:%M:%S")

        # Query DB
        result = query_db_values(converted_start_time, converted_end_time, DATABASE)
        return result


# Add API endpoint
api.add_resource(SwpcAPI, '/spwcdata/<start_date_time>/<end_date_time>')


# Get the SWPC data and return it as JSON.
def get_swpc_json(noaa_url):
    print("Attempting to retrieve SWPC data from NOAA ...")
    try:
        swpc_data = requests.get(noaa_url)

        # Load file from local filesystem to increase testing speed.
        # df = pd.read_json("noaa.json")
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
    # Pandas handles the transform of JSON to SQL and resampling.
    try:
        df = pd.DataFrame(swpc_json_data)

        # Below can be used for local filesystem testing
        # df = pd.read_json("noaa.json")

        # Set the time_tag as correct type
        df['time_tag'] = pd.to_datetime(df['time_tag'])

        # Resample data into 5 minute blocks for averaging.
        df = df.resample("5T", on='time_tag').mean()

        print("Creating and populating new", db)
        conn = sqlite3.connect(db)
        df.to_sql("swpcdata", conn)
        conn.commit()
    except ValueError:
        print("Invalid JSON data received. Cannot convert to DB. Aborting.")
        sys.exit(1)
    except Exception as E:
        print("Failed to connect", E)
        sys.exit(1)
    finally:
        # Close DB connection.
        conn.close()


# Query values from the db between the start and end times.
# The maximum query range is 1 hour
def query_db_values(start_time, end_time, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        # Retrieve values between times.
        cur.execute('SELECT * FROM swpcdata WHERE time_tag >= ? AND time_tag <= ?', (start_time, end_time))

        # Get the headers to build a JSON object
        row_headers = [header[0] for header in cur.description]  # this will extract row headers
        data_between_times = []
        for row in cur.fetchall():
            data_between_times.append(dict(zip(row_headers, row)))
        return data_between_times
    except Exception as E:
        print("Failed to connect", E)
        sys.exit(1)
    finally:
        # Close DB connection.
        conn.close()


if __name__ == '__main__':
    # Get SWPC data
    swpc_json_data = get_swpc_json(NOAA_URL)

    # Below can be uncommented for getting test data from local filesystem
    # swpc_json_data = ''

    # Create SQLite3 table from JSON data
    create_swpc_db(DATABASE, swpc_json_data)

    # Run API and wait for requests
    print("Starting webserver and waiting for request ...")

    # Running in debug mode for easy pretty print of JSON data
    app.run(debug=True)
