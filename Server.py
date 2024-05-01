from asyncio import Handle
import socket
import threading
import os
import subprocess
from tkinter import INSERT
from manipulateDB import insert_into_project, get_recent_project
from random import randrange
from pathlib import Path
import zipfile

def renderFile(blend_file, start_frame, end_frame, client_socket, downloads_folder):
    # Assuming you have blender_path, output_dir, and blend_file defined elsewhere
    blender_path = '../../../../Program Files/Blender Foundation/Blender 3.6/blender.exe' # relative path to the blender executable file 
    print('after blender path')
    outputFilePath = os.path.join(downloads_folder,"#####")
    print('after outputFilePath')
    command_string = f'"{blender_path}" -b "{blend_file}" -o "{outputFilePath}"  -s {start_frame} -e {end_frame} -E CYCLES -F PNG' # creates the command string we will use for rendering in command prompt
    print('after command_string')
    # Execute the command
    subprocess.run(command_string, shell=True)
    
def zipFile():
    print('place holder') 

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
        renderFile(filepath, start_frame, end_frame, client_socket, downloads_folder)
        # zipFile()
        # insert_into_project(randrange(9999), address, filepath, (end_frame - start_frame), start_frame, end_frame, False) # def insert_into_project(projectID, client, project_name, ames_total, start_frame, end_frame, completed):
    except Exception as e:
        print(f"An error occurred:{e}") # prints any exceptions that may come from the code
        
def handle_proletarian(prol, address,downloads_folder):
    print(f'Worker computer: {address} has connected')
    while True:
        renderProject = get_recent_project() # projectID, project_name, start_frame, end_frame

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
            # role = str(client_socket.recv(1024).decode())
            # personal note: perhaps we would want to move these identifier if conditions to a separate function that gets called?
#            if role == 'client':
#                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, downloads_folder))
#                client_thread.start()
#           if role == 'worker':
#               proletarian_thread = threading.Thread(target= handle_proletarian, args = (client_socket, addr, downloads_folder))
#               proletarian_thread.start()
#               print('place holder
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, downloads_folder))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") # tells us amount of active connections
    except Exception as e:
        print(f'An error occurred: {e}')


HOST = socket.gethostbyname(socket.gethostname())  # Server's IP. Use '0.0.0.0' to accept connections from all IPs
PORT = 65432        # Port to listen on
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")  # Path to the folder where files will be saved
print(HOST) # prints the server IP address
start_server(HOST, PORT, DOWNLOADS_FOLDER)