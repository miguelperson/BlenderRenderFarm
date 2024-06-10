from asyncio import Handle
import socket
import threading
import os
import subprocess
from tkinter import INSERT
# from manipulateDB import insert_into_project, get_recent_project
from random import randrange
from pathlib import Path
import zipfile
import sqlite3
import queue

HOST = socket.gethostbyname(socket.gethostname())  # Server's IP. Use '0.0.0.0' to accept connections from all IPs
PORT = 65432  # Port to listen on
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")  # Path to the folder where files will be saved
print(HOST)  # prints the server IP address
HEADER = 1024
FORMAT = 'utf-8'
framesToRender = queue.Queue()
renderingFlag = False
currentProject = None

conn = sqlite3.connect('render_farm.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, username TEXT, projectName TEXT, filePath TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS completedProjects (id INTEGER PRIMARY KEY, username TEXT, filepath)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS blenderProjects (id INTEGER PRIMARY KEY, username TEXT, file_path TEXT, start_frame INTEGER, end_frame INTEGER, completed BOOLEAN)''')
conn.commit()

class ActiveProject:
    def __init__(self,fileName,filePath,username):
        self.fileName = fileName
        self.fileName = filePath
        self.username = username

def set_project_active(fileName, filePath, username):
    global currentProject
    currentProject = ActiveProject(fileName, filePath, username)

def clear_currentProject():
    global currentProject
    currentProject = None

def renderFile(filepath, start_frame, downloads_folder):
    blender_path = '../../../../Program Files/Blender Foundation/Blender 4.1/blender.exe'  # relative path to the blender executable
    outputFilePath = os.path.join(downloads_folder, "####")
    # Construct the command string using the corrected output location
    command_string = f'"{blender_path}" "{filepath}" -o "{outputFilePath}" -b -f {start_frame} -E CYCLES -- --cycles-device CUDA+CPU'
    # Execute the command
    subprocess.run(command_string, shell=True)
    print(f"Rendering completed: Files are saved in {downloads_folder}")


def zipProject(downloads_folder, fileName):
    temp = fileName.split('.')
    projName = temp[0]
    zip_file_path = os.path.join(downloads_folder, f"{projName}.zip")

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(downloads_folder):
            for file in files:
                if file.endswith(".png"):  # Assuming rendered frames are PNG files, adjust the extension if necessary
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, downloads_folder))
                    os.remove(file_path)  # Delete the file after zipping
    return zip_file_path

def handle_client(client_socket, address, downloads_folder, username):
    print(f"Connected to {address}")  # prints the ip of the client that connected
    try:
        # Receive file info (filename and filesize)
        file_info = client_socket.recv(1024).decode()  # recieve the file info from client
        filename, filesize, start_frame, end_frame = file_info.split(';')
        filename = os.path.basename(filename)  # Ensure filename is just a name, not a path
        filesize = int(filesize)
        start_frame = int(start_frame)
        end_frame = int(end_frame)
        if filename == '!DISCONNECT':
            client_socket.socket.close
            return
        confirmation_message = "INFO_RECEIVED"
        client_socket.send(confirmation_message.encode())  # informs client that file info was recieved
        # Prepare to receive the file
        filepath = os.path.join(downloads_folder, filename)
        with open(filepath, 'wb') as f:  # opens file path location in write byte mode
            bytes_received = 0  # will keep track of the recieved bytes
            while bytes_received < filesize:  # so long as the bytes_recieved is less than the indicated filesize
                chunk = client_socket.recv(4096)  # recieve 4096 more bytes
                if not chunk:  # if the chunk ends up not being the full 4096 bytes
                    break  # finishes recieving
                f.write(chunk)  # writes to file
                bytes_received += len(chunk)  # would just append whats left at this point
        print(f"File {filename} has been received and saved.")
        projectDB = 'INSERT INTO blenderProjects VALUES (username,filename,filepath)'
        cursor.execute(projectDB)
        conn.commit()
    except Exception as e:
        print(f"An error occurred:{e}")  # prints any exceptions that may come from the code

def handle_proletarian(prol, address, downloads_folder):
    print(f'Worker computer: {address} has connected')
    while True:
        print('place holder')

def render_manager():
    while True:
        if not renderingFlag: # if renderingFlag == False
            cursor.execute('SELECT * FROM blenderProjects ORDER BY id ASC LIMIT 1') # blenderProjects (id INTEGER PRIMARY KEY, username TEXT, file_path TEXT, start_frame INTEGER, end_frame INTEGER, completed BOOLEAN)
            project = cursor.fetchone()
            if project: # recieved info is not null
                project_id, username, file_path, start_frame, end_frame, statusBoolean = project
                

def start_server(host, port, downloads_folder):
    DOWNLOADS_FOLDER = str(Path.home() / "Downloads")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    renderManager = threading.Thread(target=render_manager)
    renderManager.start()
    try:
        while True:
            client_socket, addr = server.accept()
            role = client_socket.recv(HEADER).decode(FORMAT)
            if role == 'worker':
                client_thread = threading.Thread(target=handle_proletarian, args= (client_socket,addr, DOWNLOADS_FOLDER))
                client_thread.start()
            if role == 'client':
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, DOWNLOADS_FOLDER))
                client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # tells us amount of active connections
    except Exception as e:
        print(f'An error occurred: {e}')


start_server(HOST, PORT, DOWNLOADS_FOLDER)