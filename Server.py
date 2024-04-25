import socket
import threading
import os
import subprocess
from tkinter import INSERT
from manipulateDP import insert_into_project
from random import randrange

def renderFile(filepath, start_frame, end_frame):
    # Assuming you have blender_path, output_dir, and blend_file defined elsewhere
    blender_path = "C:/Program Files/Blender Foundation/Blender 4.1/blender.exe"
    blend_file = filepath
    output_dir = os.path.dirname(filepath)  # Output to the same directory as the received file
    command_string = f'"{blender_path}" "{blend_file}" -b -s {start_frame} -e {end_frame} -a -o "{os.path.join(output_dir, "###")}"'
    # Execute the command
    subprocess.run(command_string, shell=True)

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
        if filename == '!DISCONNECT':
            client_socket.socket.close
            return
        confirmation_message = "INFO_RECEIVED"
        client_socket.send(confirmation_message.encode()) # informs client that file info was recieved
        # Prepare to receive the file
        filepath = os.path.join(downloads_folder, filename)
        with open(filepath, 'wb') as f: # opens file path location in write byte mode
            bytes_received = 0 # will keep track of the recieved bytes
            while bytes_received < filesize: # so long as the bytes_recieved is less than the indicated filesize
                chunk = client_socket.recv(4096) # recieve 4096 more bytes
                if not chunk: # if the chunk ends up not being the full 4096 bytes
                    break  # finishes recieving
                f.write(chunk) # writes to file
                bytes_received += len(chunk) # would just append whats left at this point
        print(f"File {filename} has been received and saved.")
        insert_into_project(randrange(9999), address, filepath, (end_frame - start_frame), start_frame, end_frame, False) # def insert_into_project(projectID, client, project_name, ames_total, start_frame, end_frame, completed):
        # renderFile(filepath, start_frame, end_frame)
    except Exception as e:
        print(f"An error occurred:{e}") # prints any exceptions that may come from the code
        
def handle_proletarian(prol, address):
    print('placeholder')

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
            role = client_socket.recv(1024).decode()
            if role == 'client':
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, downloads_folder))
                client_thread.start()
            if role == 'worker':
                print('place holder for handle worker code')
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") # tells us amount of active connections
    except Exception as e:
        print(f'An error occurred: {e}')


HOST = socket.gethostbyname(socket.gethostname())  # Server's IP. Use '0.0.0.0' to accept connections from all IPs
PORT = 65432        # Port to listen on
DOWNLOADS_FOLDER = "C:/Users/Miguel2/Downloads/testfolder"  # Path to the folder where files will be saved
print(HOST) # prints the server IP address
start_server(HOST, PORT, DOWNLOADS_FOLDER)