import asyncio
import websockets
import websockets.exceptions  # For handling handshake errors
import requests  # Added for REST API call
from csv_utils.csv_handler import df_aggregate_volume_to_csv, process_data
from config import BACKEND_HOST, BACKEND_PORT

# Handle incoming WebSocket messages
async def handle_connection(websocket):
    print("WebSocket connection established")
    try:
        while True:
            # Wait for a message from the client
            data = await websocket.recv()
            print(f"Received data (first 50 chars): {str(data)[:50]}")

            # Process the data into a DataFrame
            df = process_data(data)
            print("DataFrame created")

            # Caculate volume and output csv
            df_aggregate_volume_to_csv(df)
            print("Volume aggregated and saved to CSV")

            # Signal to REST API to update
            try:
                response = requests.post(f"{BACKEND_HOST}:{BACKEND_PORT}/notify_update")
                print(f"Signaled update to REST API, response status: {response.status_code}")
            except requests.RequestException as e:
                print(f"Failed to signal update to REST API: {e}")

            # Example: Send a response back to the client
            response = {
                "Status": 200,
            }
            await websocket.send(str(response))
    except websockets.exceptions.InvalidHandshake as e:
        print(f"Invalid WebSocket handshake: {e}")
    except websockets.ConnectionClosed:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Error: {e}")

# Start the WebSocket server
async def start_websocket_server(host="127.0.0.1", port=8765):
    print(f"Starting WebSocket server on {host}:{port}")
    async with websockets.serve(handle_connection, host, port):
        await asyncio.Future()  # Run forever

# Entry point for running the WebSocket server
if __name__ == "__main__":
    asyncio.run(start_websocket_server())
