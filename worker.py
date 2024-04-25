# this file will hold the code used by the worker computers
from http import client
import random
import socket
import os
import socket
import subprocess
from pathlib import Path
import threading

worker = None
FORMAT = 'utf-8'
HEADER = 1024
confirmation_message = 'INFO_RECIEVED'

def connect():
    HOST = '192.168.99.124'
    PORT = 65432
    ADDR = (HOST, PORT)
    worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker.connect(ADDR) # connects to the server
    worker.sendall(b'worker')
    worker_IP = socket.gethostbyname(socket.gethostbyname)
    return worker


def render_third_frame(blender_path, filePath): # render function responsible for processing and rendering the photos
    # Extract the directory from the blend file path
    output_dir = os.path.dirname(blend_file) # saves output folder file path

    # Ensure paths are enclosed in quotes
    command_string = f'"{blender_path}" "{blend_file}" -b -f 35 -o "{os.path.join(output_dir, "###")}"' # creates the command string we will use for rendering in command prompt

    subprocess.run(command_string, shell=True)  # Added shell=True for executing the command string
    print(output_dir)
    
def waitForCommand(worker, downloads_path, blender_path):
    while True:
        fileInfo = worker.recv().decode(HEADER) # name;file size
        fileName, fileSize = fileInfo.split(';')
        worker.send(confirmation_message.encode()) # send
        filePath = os.path.join(downloads_path, fileName)
        with open(filePath, 'wb') as f: # recieve the blend file
            bytes_recieved = 0
            while bytes_recieved < fileSize:
                chunk = worker.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                bytes_recieved += len(chunk)
        worker.send(confirmation_message.encode) # send
        renderThread = threading.Thread(target = render_third_frame, args =(blender_path, filePath))
        renderThread.start()
        
        
        

def main(): # will need to change functions to allow for server to send data to worker computer
    blender_path = '../../../../Program Files/Blender Foundation/Blender 3.6/blender.exe' # relative path to the blender executable file location
    downloads_path = str(Path.home() / "Downloads")
    worker = connect()
    waitForCommand(worker, downloads_path, blender_path)