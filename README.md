# meat-slicer-backend

This repository contains the backend for the Meat Slicer application. It includes a Flask-based REST API, a WebSocket server for real-time communication, and Arduino integration for conveyor control.

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package manager)
- Arduino IDE (if working with Arduino hardware)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd meat-slicer-backend
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backend

### 1. Start the Flask REST API

The Flask application provides REST API endpoints for handling requests.

Run the following command:
```bash
python app.py
```

The API will be available at `http://127.0.0.1:8000`.

### 2. Start the WebSocket Server

The WebSocket server handles real-time communication and processes incoming data.

Run the following command:
```bash
python websocket_server.py
```

The WebSocket server will be available at `ws://127.0.0.1:8765`.

### 3. Start the Conveyor Control System

The conveyor control system integrates with Arduino to manage the conveyor's operation.

Run the following command:
```bash
python main.py
```

This script initializes the Arduino, starts the conveyor, and listens for signals from the Arduino to stop or resume the conveyor.

## File Structure

- `app.py`: Entry point for the Flask REST API.
- `websocket_server.py`: WebSocket server for real-time communication.
- `main.py`: Conveyor control system with Arduino integration.
- `routes/`: Contains route definitions for the Flask API.
- `csv_utils/`: Utilities for handling CSV operations.
- `websocket/`: Utilities for processing WebSocket data.

## Notes

- Ensure the Arduino is properly connected and configured before running `main.py`.
- The WebSocket server sends updates to the REST API at `http://127.0.0.1:8000/notify_update` when new data is processed.
- Modify the `WEBSITE_SERVER` and `BACKEND_PORT` in the `.env` file as needed for your setup.

## Troubleshooting

- If you encounter issues with dependencies, ensure all required packages are installed using `pip install -r requirements.txt`.
- For Arduino-related issues, verify the Arduino is connected and the correct port is specified in the code.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.