import moonrakerpy as moonpy
from config import MOONRAKER_HOST, X_VORON_START_POS, Y_VORON_START_POS
import time
import requests

# Voron Home
# X20 Y270

class VoronController:
    def __init__(self, host=MOONRAKER_HOST):
        self.client = moonpy.MoonrakerPrinter(host)

    def send_xyz_coordinates(self, x, y):
        # Adjust coordinates based on the Voron home position
        x_abs = X_VORON_START_POS + x
        y_abs = Y_VORON_START_POS - y
        command = f"G1 X{x_abs} Y{y_abs} F6000"
        response = self.client.send_gcode(command)
        print(f"Sent command: {command}")
        print(f"Received response: {response}")
        return response

    def close_connection(self):
        print("No persistent connection to close with Moonraker.")

    def is_status_idle(self):
        while True:
            try:
                response = requests.get(f"{MOONRAKER_HOST}/printer/objects/query?motion_report")
                if response.status_code != 200:
                    print("Error fetching status from Moonraker")
                    time.sleep(0.2)
                    continue

                status = response.json()
                live_velocity = status['result']['status']['motion_report']['live_velocity']
                if live_velocity == 0:
                    return True
            except Exception as e:
                print(f"Error querying Moonraker: {e}")
            time.sleep(0.1)

    def process_cut_positions(self, cut_positions, belt_speed=21, voron_speed=30):
        """
        Process the given cut positions, adjusting for conveyor movement and Voron movement speed.
        :param cut_positions: List of cut positions with axis_position, start_cut_position, and end_cut_position.
        :param belt_speed: Speed of the conveyor belt in mm/s.
        :param voron_speed: Speed of the Voron in mm/s.
        """
        last_time = time.time()
        belt_offset = 0

        # Flatten the cut queue into individual movements
        movement_queue = []
        for position in cut_positions:
            movement_queue.append({
                "axis_position": position["axis_position"],
                "y_position": position["start_cut_position"]
            })
            movement_queue.append({
                "axis_position": position["axis_position"],
                "y_position": position["end_cut_position"]
            })

        for i, movement in enumerate(movement_queue):
            # Calculate elapsed time and update belt offset
            current_time = time.time()
            elapsed_time = current_time - last_time
            belt_offset += belt_speed * elapsed_time
            last_time = current_time

            # Adjust axis_position (X-axis) with the belt offset
            adjusted_axis_position = movement["axis_position"] + belt_offset

            # Calculate Voron movement time
            if i > 0:
                prev_movement = movement_queue[i - 1]
                distance = abs(adjusted_axis_position - (prev_movement["axis_position"] + belt_offset))
                voron_movement_time = distance / voron_speed
                belt_offset += belt_speed * voron_movement_time

            # Send adjusted position to Voron
            self.send_xyz_coordinates(adjusted_axis_position, movement["y_position"])
            while not self.is_status_idle():
                time.sleep(0.1)
