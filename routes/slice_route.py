from flask import Blueprint, jsonify, request
from process.helper import create_slice_dict, volume_aggregator
from config import *
from csv_utils.csv_handler import get_volume_from_csv
from voron.voron_controller import VoronController
import time

slicing_routes = Blueprint("slicing", __name__)
voron = VoronController()

@slicing_routes.route("/slice", methods=["POST"])
def slice_data():
    # Parse the request data
    data = request.json
    axis = data.get("axis")
    slices = data.get("slices")
    print(f"Slicing request received: axis={axis}, slices={slices}")

    df, volume = get_volume_from_csv(PREPROCESSED_FILEPATH)
    df = df.iloc[:-1]  # Disregard the last row of the DataFrame

    # Create slice dictionary
    slice_data = create_slice_dict(
        num_slices=slices, volume=volume, cut_axis=axis
    )
    print(f"Slice data created: {slice_data}")
    cut_positions = volume_aggregator(df, slice_data=slice_data)
    
    response_data = {
        "message": "Slicing request processed successfully",
        "axis": axis,
        "slices": slices,
        "slice_data": slice_data,
        "volume": volume,
    }

    # Pass calculated cut positions to VORON
    voron.process_cut_positions(cut_positions)

    # Signal slicing process completion
    flag_file = 'slicing_done.flag'
    with open(flag_file, 'w') as f:
        f.write('Slicing completed')
    print(f"Flag file '{flag_file}' created.")

    return jsonify(response_data)

@slicing_routes.route("/get_slices", methods=["POST"])
def get_slices():
    data = request.json
    num_slices = data["num_slices"]
    slice_positions = [{"x": i * 10} for i in range(1, num_slices + 1)]
    return jsonify(slice_positions)
