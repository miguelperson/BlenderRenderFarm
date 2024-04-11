import socket
import threading
import os
def handle_client(client_socket, address, downloads_folder):
    print(f"Connected to {address}") # prints the ip of the client that connected
    try:
        # Receive file info (filename and filesize)
        file_info = client_socket.recv(1024).decode() # recieve the file info from client, is holding code, will wait here until client sends code
        filename, filesize, start_frame, end_frame = file_info.split(';') # saves each corresponding attribute to their respective variable
        filename = os.path.basename(filename)  # Ensure filename is just a name, not a path
        filesize = int(filesize)
        start_frame = int(start_frame)
        end_frame = int(end_frame)

        confirmation_message = "INFO_RECEIVED"
        client_socket.send(confirmation_message.encode()) # informs client that file info was recieved
        # Prepare to receive the file
        filepath = os.path.join(downloads_folder, filename)
        with open(filepath, 'wb') as f: # opens file path location in write byte mode
            bytes_received = 0 # will keep track of the recieved bytes
            while bytes_received < filesize: # so long as the bytes_recieved is less than the indicated filesize
                chunk = client_socket.recv(4096) # recieve 4096 more bytes
                if not chunk: # if the chunk ends up not being the full 4096 bytes
                    break  # connection closed
                f.write(chunk) # finishes writing the 
                bytes_received += len(chunk) # would just append whats left at this point
        print(f"File {filename} has been received and saved.")
    finally:
        client_socket.close

def start_server(host, port, downloads_folder):
    # Ensure the downloads folder exists
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder) # makes folder if folder dose not exist
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