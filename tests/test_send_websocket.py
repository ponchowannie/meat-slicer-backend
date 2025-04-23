import asyncio
import websockets

async def test_websocket_client():
    uri = "ws://127.0.0.1:8765"  # WebSocket server address
    try:
        # Connect to the WebSocket server
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")

            # Example data to send (e.g., CSV-like data for processing)
            data_to_send = "0.1,0,1,2\n0.1,1,2,3\n0.2,3,4,6\n0.3,7,8,9"
            print(f"Sending data:\n{data_to_send}")
            
            # Send the data to the server
            await websocket.send(data_to_send)

            # Wait for a response from the server (optional)
            response = await websocket.recv()
            print(f"Received response from server: {response}")
    except Exception as e:
        print(f"Error: {e}")

# Run the WebSocket client
if __name__ == "__main__":
    asyncio.run(test_websocket_client())