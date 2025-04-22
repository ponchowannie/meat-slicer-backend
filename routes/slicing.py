from flask import Blueprint, jsonify, request

slicing_routes = Blueprint("slicing", __name__)

@slicing_routes.route("/slice", methods=["POST"])
def slice_data():
    data = request.json
    axis = data.get("axis")
    slices = data.get("slices")
    print(f"Slicing request received: axis={axis}, slices={slices}")
    response_data = {
        "message": "Slicing request processed successfully",
        "axis": axis,
        "slices": slices,
    }
    return jsonify(response_data)

@slicing_routes.route("/get_slices", methods=["POST"])
def get_slices():
    data = request.json
    num_slices = data["num_slices"]
    slice_positions = [{"x": i * 10} for i in range(1, num_slices + 1)]
    return jsonify(slice_positions)
