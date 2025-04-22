import serial
import time

arduino = None

def initialize_arduino():
    global arduino
    # Arduino port (Linux/macOS: '/dev/ttyUSB0' or '/dev/ttyACM0')
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
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
            if message == "DETECTED":
                stop_conveyor()
                stop_event.set()