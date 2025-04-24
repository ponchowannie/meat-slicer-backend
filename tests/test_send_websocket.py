import asyncio
import websockets
import csv
from config import WEBSOCKET_ENDPOINT

async def test_websocket_client():
    uri = WEBSOCKET_ENDPOINT  # WebSocket server address
    try:
        # Read and process the CSV file
        csv_file_path = "./files/extracted_data.csv"
        formatted_data = []
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                formatted_data.append(",".join(row))
        data_to_send = "\n".join(formatted_data)

        print(f"Sending data:\n{data_to_send}")

        # Connect to the WebSocket server
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            
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