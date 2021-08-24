# Task 2 - Data handling and basic Visualisation test
# Plot the 20 minute moving average of GOES-16 Flux data against its raw inputs.
import sys

import pandas as pd
import matplotlib.pyplot as plt


def load_json_data(json_file):
    try:
        df = pd.read_json(json_file)
    except ValueError:
        print(json_file + " is not found. Please check file exists and is named correctly.")
        sys.exit(1)
    return df


if __name__ == '__main__':

    # File path/name containing Proton JSON data.
    PROTON_DATA_FILE = "differential-protons-1-day.json"
    # Rolling average of 20 Minutes. Every 1 sample is 5 minutes apart.
    MOVING_AVERAGE = 5

    # Read in JSON to Panda DataFrame.
    df = load_json_data(PROTON_DATA_FILE)

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
    time_flux_average_df.plot()
    plt.show()

