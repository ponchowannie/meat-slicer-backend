import serial
import time
from config import *

arduino = None

def initialize_arduino():
    global arduino
    # Arduino port (Linux/macOS: '/dev/ttyUSB0' or '/dev/ttyACM0')
    arduino = serial.Serial(port=ARDUINO_PORT, baudrate=ARDUINO_BAUDRATE, timeout=ARDUINO_TIMEOUT)
    time.sleep(2)  # Give Arduino time to reset

def send_command(command):
    # Send command to Arduino as bytes
    arduino.write((command + '\n').encode())
    print(f"Sent: {command}")

def start_conveyor():
    send_command("START")

def stop_conveyor():
    send_command("STOP")

def close_conveyor_conn():
    arduino.close()

def listen_to_arduino(stop_event):
    while not stop_event.is_set():
        if arduino.in_waiting > 0:
            message = arduino.readline().decode('utf-8').rstrip()
            print(f"Received from Arduino: {message}")
            if message == "PASSED":
                # stop_conveyor()
                print("Stop Conveyor") # Arduino Side
                stop_event.set()