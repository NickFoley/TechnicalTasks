# Task 2 - Data handling and basic Visualisation test
# Plot the 20 minute moving average of GOES-16 Flux data against its raw inputs.
import sys

import pandas as pd
import matplotlib.pyplot as plt
import requests


# Get JSON data from json_url and load it into a Pandas DataFrame
def load_json_data(json_url):
    print("Attempting to retrieve GOES data ...")
    try:
        data = requests.get(json_url)
        df = pd.DataFrame(data.json())
    except Exception as E:
        print("Failed to retrieve GOES data", E)
        sys.exit(1)
    print("Data successfully received.")

    # Uncomment to load proton data from local file instead of remotely.
    # try:
    #     df = pd.read_json(json_url)
    # except ValueError:
    #     print(json_url + " is not found. Please check file exists and is named correctly.")
    #     sys.exit(1)
    return df


if __name__ == '__main__':
    # Constants
    # Rolling average of 20 Minutes. Every 1 sample is 5 minutes apart. 20/5 = average across 4 samples.
    MOVING_AVERAGE = 4
    GOES_URL = 'https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json'

    # Load file from local filesystem to increase testing speed.
    # File path/name containing Proton JSON data.
    # GOES_URL = "differential-protons-1-day.json"

    # Read in JSON to Panda DataFrame.
    df = load_json_data(GOES_URL)

    # Set the DataFrame index to the datetime.
    df.set_index("time_tag", inplace=True)

    # Filter data just for Channel = P1.
    p_channel_df = df[df["channel"] == "P1"]

    # Remove unneeded data, just keep flux and the index (datetime).
    time_flux_df = p_channel_df[["flux"]]

    # Inject a rolling average
    # Copy created to avoid potentially unexpected settingWithCopy warning/behaviour.
    time_flux_average_df = time_flux_df.copy()
    time_flux_average_df["moving_average"] = time_flux_df.flux.rolling(MOVING_AVERAGE, min_periods=1).mean()

    # Plot the rolling average and raw data against time
    time_flux_average_df.plot(xlabel='Datetime', ylabel='Flux', title='GOES 16 Proton Flux vs Datetime')
    plt.show()
