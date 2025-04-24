from flask import Blueprint, jsonify, Response
import json
import queue
from utils.point_cloud_loader import load_data
from time import time

point_cloud_routes = Blueprint("point_cloud", __name__)
sse_queue = queue.Queue()

@point_cloud_routes.route("/get_point_cloud", methods=["GET"])
def get_point_cloud():
    """
    Endpoint to fetch the current point cloud data.
    """
    return jsonify(load_data())

@point_cloud_routes.route("/notify_update", methods=["POST"])
def notify_update():
    """
    Internal endpoint to notify clients of updates by adding a message to the SSE queue.
    """
    print("Update notification received")
    update_data = load_data()
    sse_queue.put(update_data)  # Add the raw data (not serialized) to the queue
    return jsonify({"message": "Update notification sent"})

@point_cloud_routes.route("/events", methods=["GET"])
def sse():
    """
    SSE endpoint for clients to receive real-time updates.
    """
    def event_stream():
        while True:
            try:
                # Wait for updates from the queue
                update = sse_queue.get(timeout=10)
                # Serialize the data as a JSON string before sending
                yield f"data: {json.dumps(update)}\n\n"
            except queue.Empty:
                # Send a heartbeat to keep the connection alive
                yield f"data: []\n\n"  # Send an empty JSON array as a heartbeat
            except GeneratorExit:
                # Handle client disconnection gracefully
                print("Client disconnected from SSE")
                break
            except Exception as e:
                # Log unexpected errors and break the loop
                print(f"Unexpected error in SSE stream: {e}")
                break

    # Ensure headers for SSE are set properly
    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }
    return Response(event_stream(), headers=headers)
