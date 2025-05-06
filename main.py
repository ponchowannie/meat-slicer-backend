from conveyor import start_conveyor, stop_conveyor, initialize_arduino, listen_to_arduino
import threading
import time
import os

def main():
    # Initialize Arduino
    initialize_arduino()
    stop_event = threading.Event()

    while True:
        # Start the conveyor
        start_conveyor()

        # Start listening to Arduino in a separate thread
        arduino_thread = threading.Thread(target=listen_to_arduino, args=(stop_event,))
        arduino_thread.start()

        # Wait for the Arduino listener to signal a stop
        arduino_thread.join()

        # Wait for the slicing process to finish
        flag_file = 'slicing_done.flag'
        while not os.path.exists(flag_file):
            print("Waiting for slicing process to finish...")
            time.sleep(1)

        # Remove the flag file after detecting it
        os.remove(flag_file)
        print("Slicing process completed. Resuming conveyor...")

        # Reset the stop event and resume the conveyor
        stop_event.clear()
        print("Resuming conveyor process...")

if __name__ == "__main__":
    main()