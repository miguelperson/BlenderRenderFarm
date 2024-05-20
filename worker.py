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
HEADER = 1024
confirmation_message = 'INFO_RECEIVED'

def connect():
    HOST = '192.168.99.124'
    PORT = 65432
    ADDR = (HOST, PORT)
    worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker.connect(ADDR) # connects to the server
    worker.sendall(b'worker')
    return worker


def render_third_frame(worker, blender_path, filePath, downloads_path): # render function responsible for processing and rendering the photos
    frameToRender = int(worker.recv().decode(HEADER)) # recieves int indicating what frame to render
    worker.send(confirmation_message.encode()) # send confirm
    # Ensure paths are enclosed in quotes
    outputFilePath = os.path.join(downloads_path,"#####")
    command_string = f'"{blender_path}" -b "{filePath}" -o "{outputFilePath}"  -f {frameToRender} -E CYCLES -F PNG' # creates the command string we will use for rendering in command prompt
    subprocess.run(command_string, shell=True)
    outputFileName = f'{frameToRender:05d}'+'.png'
    renderFilePath = downloads_path+'\\'+outputFileName
    if not os.path.isfile(renderFilePath): # checks if file exists
        print(f"File not found: {renderFilePath}")
        return
    fileSize = os.path.getsize(renderFilePath)
    fileInfo = f'{outputFileName};{fileSize}'
    worker.sendall(fileInfo) # send filename;filesize
    confirmation = worker.recv(HEADER).decode() # recieve confirmation
    if confirmation == "INFO_RECIEVED":
        with open(renderFilePath,'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                worker.sendall(bytes_read) # send
    os.remove(renderFilePath)
    
    
def waitForCommand(worker, downloads_path, blender_path):
    while True:
        fileInfo = worker.recv().decode(HEADER) # name;file size
        fileName, fileSize = fileInfo.split(';')
        worker.send(confirmation_message.encode()) # send
        filePath = os.path.join(downloads_path, fileName) #.../downloads/'filename'
        with open(filePath, 'wb') as f: # recieve the blend file
            bytes_recieved = 0
            while bytes_recieved < fileSize:
                chunk = worker.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                bytes_recieved += len(chunk)
        worker.send(confirmation_message.encode) # recieve confirmation
        renderThread = threading.Thread(target = render_third_frame, args =(worker, blender_path, filePath, downloads_path))
        renderThread.start()
        
        
        

def main(): # will need to change functions to allow for server to send data to worker computer
    blender_path = '../../../../Program Files/Blender Foundation/Blender 3.6/blender.exe' # relative path to the blender executable file location
    downloads_path = str(Path.home() / "Downloads")
    worker = connect()
    waitForCommand(worker, downloads_path, blender_path)