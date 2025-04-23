import numpy as np
import pandas as pd
from config import *
from .edge_padding import pad_edges

# Keep this file for data loading logic. Ensure it only contains reusable functions.
def load_data():
    df = pd.read_csv(CSV_FILEPATH, header=None)
    print(f"Length of df {df.shape[0]} {df.shape[1]}")
    points = []
    edges = []

    # Get the x values from the first row (excluding the first element)
    x_values = df.iloc[0, :].values

    # Get the y values from the first column (excluding the first element)
    y_values = df.iloc[:, 0].values

    # Extract the depth values (excluding the first row and column)
    depth_values = df.iloc[1:, 1:].values

    # Create a mask for non-zero depths
    non_zero_mask = (depth_values > 0)

    # Create a padded version of the depth array to check neighbors efficiently
    padded_depth = np.pad(depth_values, pad_width=1, mode='constant', constant_values=0)

    # Identify edges by checking if any neighbor is zero
    edge_mask = (
        (padded_depth[1:-1, :-2] == 0) |  # Left
        (padded_depth[1:-1, 2:] == 0) |   # Right
        (padded_depth[:-2, 1:-1] == 0) |  # Up
        (padded_depth[2:, 1:-1] == 0)     # Down
    ) & non_zero_mask

    # Collect points and edges
    for x_idx, y_idx in zip(*np.where(non_zero_mask)):
        x_value = x_values[y_idx + 1]  # Adjust index for x_values
        y_value = y_values[x_idx + 1]  # Adjust index for y_values
        depth = depth_values[x_idx, y_idx]

        points.append({"x": x_value, "y": y_value, "z": depth})
        points.append({"x": x_value, "y": y_value, "z": 0})

        if edge_mask[x_idx, y_idx]:
            edges.append({"x": x_value, "y": y_value, "z": depth})

    print(f"Length of edges {len(edges)}")
    points = pad_edges(points, edges, depth_increment=DEPTH_INCREMENT)

    return points