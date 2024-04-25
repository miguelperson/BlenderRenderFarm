# this file will hold the code used by the worker computers
from http import client
import random
import socket
import os
import socket

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


def render_third_frame(blender_path, blend_file): # render function responsible for processing and rendering the photos
    # Extract the directory from the blend file path
    output_dir = os.path.dirname(blend_file) # saves output folder file path

    # Ensure paths are enclosed in quotes
    command_string = f'"{blender_path}" "{blend_file}" -b -f 35 -o "{os.path.join(output_dir, "###")}"' # creates the command string we will use for the

    subprocess.run(command_string, shell=True)  # Added shell=True for executing the command string

    print('hello butt stuff')
    print(output_dir)
    
def waitForCommand(worker):
    print('place holder')
    while True:
        fileInfo = worker.recv().decode(HEADER) # name;file size
        fileName, fileSize = fileInfo.split(';')
        worker.send(confirmation_message.encode())
        
        
        

def main(): # will need to change functions to allow for server to send data to worker computer
    blender_path = '../../../../Program Files/Blender Foundation/Blender 3.6/blender.exe' # relative path to the blender executable file location
    worker = connect()
    waitForCommand(worker)
    # Ask the user for the .blend file path
    blend_file = input("Enter the path to the .blend file: ")