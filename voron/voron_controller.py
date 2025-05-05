from moonrakerpy import Moonraker
from config import MOONRAKER_HOST, X_VORON_START_POS, Y_VORON_START_POS

# Voron Home
# X20 Y270

class VoronController:
    def __init__(self, host=MOONRAKER_HOST):
        self.client = Moonraker(host=host)

    def send_xyz_coordinates(self, x, y):
        # Adjust coordinates based on the Voron home position
        x_abs = X_VORON_START_POS + x
        y_abs = Y_VORON_START_POS - y
        command = f"G1 X{x_abs} Y{y_abs} F3000"
        response = self.client.send_gcode(command)
        print(f"Sent command: {command}")
        print(f"Received response: {response}")
        return response

    def close_connection(self):
        print("No persistent connection to close with Moonraker.")