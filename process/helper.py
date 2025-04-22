from config import *
from utils.utils import print_time
import time
import numpy as np

# get_slice_lane -- Helper function to get the start and end cut position
def get_slice_lane(column_values, coordinates):
    start_cut_position = None
    end_cut_position = 0
    for itr, height in enumerate(column_values):
        # Find the start cut position
        if height != 0 and start_cut_position is None:  
            start_cut_position = coordinates[itr]
        # Find the end using appearance of height = 0
        if start_cut_position and height == 0:
            end_cut_position = coordinates[itr]
    # Handle case where end cut position is the last row
    if end_cut_position == 0:
        end_cut_position = coordinates[-1]
        
    # add offset for cutting position
    print(f"Start cut position: {start_cut_position:.3f}, End cut position: {end_cut_position:.3f}")
    start_cut_position += start_cut_position * 0.1
    end_cut_position += end_cut_position * 0.1
    return start_cut_position, end_cut_position

# create_slice_dict -- Helper function to create a dictionary for slicing
def create_slice_dict(
    num_slices: int = 0, volume: float = 0.0, cut_direction: str = "X"
):
    volume_per_slice = volume / num_slices
    return {
        "slices": num_slices,
        "volume_per_slice": volume_per_slice,
        "cut_direction": cut_direction,
    }

def volume_aggregator(
    df, slice_data: dict = None
):
    # Find the start time
    start_time = time.time()
    
    # Get x, y, z values
    x_coords = df.columns.astype(float)
    y_coords = df.index.astype(float)
    z_values = df.to_numpy(float)

    # Calculate the differences between consecutive x and y coordinates
    dx = np.diff(x_coords)
    dy = np.diff(y_coords)

    is_slice = False
    if slice_data is not None:
        is_slice = True
        # slices = slice_data["slices"]
        volume_per_slice = slice_data["volume_per_slice"]
        if slice_data["cut_direction"].lower() == "y":
            dx, dy = dy, dx
            x_coords, y_coords = y_coords, x_coords
            z_values = z_values.T  # Transpose the z_values array

    # Calculate the volume using the trapezoidal rule
    total_volume = 0.0  # in mm^3
    integral_time = time.time()
    for i, dx_value in enumerate(dx[:-1]):  # per column, avoid last index
        for j, dy_value in enumerate(dy[:-1]):  # per cell in the column, avoid last index
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
                            
        if is_slice:
            if total_volume >= volume_per_slice:
                print("-----------------------------")
                start_cut_position, end_cut_position = get_slice_lane(z_values[:, i], y_coords)
                print(
                    f"Cut at {os.environ['DIR1']} position: {x_coords[i]}, "
                    f"from {os.environ['DIR2']}: {start_cut_position:.3f} to {end_cut_position:.3f} # 10% offset"
                )
                print_time(f"Accumulated volume: {total_volume/1000:.2f} cm^3", integral_time)
                integral_time = time.time()
                total_volume = 0.0  # Reset for the next slice
                
    if is_slice:
        return None
    else:
        print_time(f"The volume of the scanned object is approximately {total_volume/1000:.2f} cm^3.", start_time)
        return total_volume
