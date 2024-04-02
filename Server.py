import socket
import threading
import os
def handle_client(client_socket, address, downloads_folder):
    print(f"Connected to {address}")
    try:
        # Receive file info (filename and filesize)
        file_info = client_socket.recv(1024).decode()
        filename, filesize, start_frame, end_frame = file_info.split(';') # saves each corresponding attribute to their respective variable
        filename = os.path.basename(filename)  # Ensure filename is just a name, not a path
        filesize = int(filesize)

        confirmation_message = "INFO_RECEIVED"
        client_socket.send(confirmation_message.encode())
        # Prepare to receive the file
        filepath = os.path.join(downloads_folder, filename)
        with open(filepath, 'wb') as f:
            bytes_received = 0
            while bytes_received < filesize:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break  # connection closed
                f.write(chunk)
                bytes_received += len(chunk)
        print(f"File {filename} has been received and saved.")
    finally:
        client_socket.close

def start_server(host, port, downloads_folder):
    # Ensure the downloads folder exists
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    try:
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, downloads_folder))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") # tells us amount of active connections
    finally:
        server.close()
HOST = socket.gethostbyname(socket.gethostname())  # Server's IP. Use '0.0.0.0' to accept connections from all IPs
PORT = 65432        # Port to listen on
DOWNLOADS_FOLDER = "C:/Users/Miguel2/Downloads/testfolder"  # Path to the folder where files will be saved
print(HOST) # prints the server IP address
start_server(HOST, PORT, DOWNLOADS_FOLDER)