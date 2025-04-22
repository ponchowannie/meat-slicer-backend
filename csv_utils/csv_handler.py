from config import *
from utils.utils import print_time, execution_time
import time
import pandas as pd
import os

def extract_data_to_csv(filepath):
    # Find the start time
    start_time = time.time()

    output_file_path = "extracted_data.csv"

    # Define the row where "Y\X" is located (zero-based index)
    yx_row = 27

    # Read the CSV file, skipping rows before "Y\X"
    df = pd.read_csv(filepath, header=None, dtype=str, skiprows=yx_row)

    # Find the first occurrence of "End" in the first column
    end_row = df[df[0] == "End"].index.min()

    # Extract the relevant data up to the row before "End"
    extracted_data = df.iloc[:end_row]

    # Fill NaN values with 0
    extracted_data = extracted_data.fillna(0)

    extracted_data.to_csv(os.environ["filepath"], index=False, header=False)
    print(f"Extracted data saved to {output_file_path}")

    execution_time(start_time)
    return extracted_data

def clean_csv_file_to_df(df, x_resolution, y_resolution):
    pd.set_option('future.no_silent_downcasting', True)
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
    
    df.to_csv(os.environ["filepath"], index=True, header=True)
    print_time("Cleaned data saved to cleaned_data.csv", start_time)
    return df