import socket
import pandas as pd

# Function to process received data and convert it to a DataFrame
def process_data(data):
    # Split the data into rows based on newline or other delimiters
    rows = data.strip().split("\n")
    # Split each row into columns based on commas
    data_list = [row.split(",") for row in rows]
    # Create a DataFrame
    df = pd.DataFrame(data_list)

    return df

# Set up the socket server
def start_server(host='127.0.0.1', port=65432):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    # Listen for incoming connections
    server_socket.listen(1)
    print("-----------------------------")
    print(f"Server listening on {host}:{port}")
    
    return server_socket


def get_data_socket(server_socket: socket):
    while True:
        # Accept a connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data: {data}")

        # Process the data into a DataFrame
        df = process_data(data)
        print("DataFrame created:")
        print(df)

        # Close the client connection
        client_socket.close()
        break
    
    return df

# Start the server
if __name__ == "__main__":
    start_server()