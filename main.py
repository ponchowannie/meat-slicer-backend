from conveyor import start_conveyor, stop_conveyor, initialize_arduino, listen_to_arduino
import threading
import time

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

        # Stop the conveyor when Arduino signals
        stop_conveyor()

        # Simulate waiting for an external process to finish
        print("Waiting for external process to finish...")
        time.sleep(5)  # Replace with actual external process logic

        # Reset the stop event and resume the conveyor
        stop_event.clear()
        print("Resuming conveyor process...")

if __name__ == "__main__":
    main()