import asyncio
import websockets
from websocket.socket_handler import process_data

# Handle incoming WebSocket messages
async def handle_connection(websocket, path):
    print("WebSocket connection established")
    try:
        while True:
            # Wait for a message from the client
            data = await websocket.recv()
            print(f"Received data: {data}")

            # Process the data into a DataFrame
            df = process_data(data)
            print("DataFrame created:")
            print(df)

            # Example: Send a response back to the client
            response = {
                "Status": 200,
            }
            await websocket.send(str(response))
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
