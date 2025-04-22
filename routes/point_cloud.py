from flask import Blueprint, jsonify
from utils.loader import load_data

point_cloud_routes = Blueprint("point_cloud", __name__)

@point_cloud_routes.route("/get_point_cloud", methods=["GET"])
def get_point_cloud():
    return jsonify(load_data())
