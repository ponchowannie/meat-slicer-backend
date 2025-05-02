import sys
import os
import time
import pandas as pd
import numpy as np

# Add the parent directory to the Python path to access config globally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from utils.utils import print_time, execution_time

# Function to process received data and convert it to a DataFrame
def process_data(data):
    # Split the data into rows based on newline or other delimiters
    rows = data.strip().split("\n")
    # Split each row into columns based on commas
    data_list = [row.split(",") for row in rows]
    # Create a DataFrame
    df = pd.DataFrame(data_list)

    return df

def preprocess_df(df, x_resolution, y_resolution):
    # Find the start time
    start_time = time.time()

    # Remove the first row and first column
    df = df.iloc[1:, 1:]

    # Add the distance resolution to the column and index labels
    df.columns = [round(i * x_resolution, 3) for i in range(len(df.columns))]
    df.index = [round(i * y_resolution, 3) for i in range(len(df))]

    # Fill NaN values with 0
    df = df.fillna(0)
    df = df.infer_objects(copy=False)
    print_time("Cleaned csv data for df", start_time)
    return df

def df_aggregate_volume_to_csv(df):
    # Replace empty strings with zero
    df.replace("", 0, inplace=True)

    # Clean csv data for the df
    df = preprocess_df(df, x_resolution=0.178, y_resolution=0.338)

    # Find the start time
    start_time = time.time()

    # Get x, y, z values
    x_coords = df.columns.astype(float)
    y_coords = df.index.astype(float)
    z_values = df.to_numpy(float)

    # Calculate the differences between consecutive x and y coordinates
    dx = np.diff(x_coords)
    dy = np.diff(y_coords)

    # Calculate the volume using the trapezoidal rule
    total_volume = 0.0  # in mm^3
    for i, dx_value in enumerate(dx[:-1]):  # per column
        for j, dy_value in enumerate(dy[:-1]):  # per cell in the column
            # Calculate the average height of the four corners of the cell
            avg_height = (
                z_values[j, i]
                + z_values[j, i + 1]
                + z_values[j + 1, i]
                + z_values[j + 1, i + 1]
            ) / 4
            # Calculate the area of the cell
            cell_area = dx_value * dy_value
            # Add the volume of the cell to the total volume
            total_volume += avg_height * cell_area

    # Convert total volume from mm^3 to cm^3 and round to three decimal points
    total_volume = round(total_volume / 1000, DECIMAL_POINTS)

    # # Reset index to make y_coords a column
    df_reset = df.reset_index()
    df_reset.rename(columns={'index': '0'}, inplace=True)

    # Append the total volume as a new row (with empty x columns)
    total_row = ['Total Volume (cm^3)', total_volume] + [''] * (df_reset.shape[1] - 2)
    df_reset.loc[len(df_reset)] = total_row

    # Save the updated DataFrame back to the CSV, including y_coords as first column
    df_reset.to_csv(PREPROCESSED_FILEPATH, index=False, header=True)
    print(f"Total volume: {total_volume:.2f} cm^3")
    print_time("Total volume calculated and saved to CSV", start_time)
    return df_reset

def get_volume_from_csv(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath, header=None, dtype=str)

    # Find the row with "Total Volume (cm^3)"
    total_volume_row = df[df[0] == "Total Volume (cm^3)"]

    if not total_volume_row.empty:
        # Extract the total volume value
        total_volume = total_volume_row.iloc[0, 1]
        return df, float(total_volume)
    else:
        print("Total volume not found in the CSV file.")
        return None, None

if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("./files/extracted_data.csv", header=None, dtype=str)
    df_aggregate_volume_to_csv(df)
    df = pd.read_csv(PREPROCESSED_FILEPATH, header=None, dtype=str)
    print(df.head())