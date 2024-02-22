import socket
#import Client # allos us to use functions created within the gui code
import os
from sqlite3 import connect # imports os handling library
import threading
import subprocess

from manipulateDB import *

# server side implementation of socket 
SERVER = socket.gethostbyname(socket.gethostname()) # gets IP address of server node
port = 5050 # port 8080 is apparently for HTTPs communications so will play it safe and not run on that port here
ADDR = (SERVER,port)
HEADER = 1024 # will be the header for the data we want to send
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SAVE_PATH = r"C:\Users\Miguel2\Downloads"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create sockets, AF INET is the socket type of family which is INET
server.bind(ADDR)


def handle_client(conn, addr): # handles communication between client and server, will use mutithreading
    print(f"[NEW CONNECTION] {addr} connected.") # tells us who connected, connections will be running concurrently
    connected = True 
    while connected: # waiting to recieve information from client, connection will remain constant until disconnect message sent
        file_name = conn.recv(HEADER).decode() # the .recv() is a blocking code, will also recieve the file name first
        if file_name == DISCONNECT_MESSAGE:
            print(f"[DISCONNECTED] {addr} disconnnected from the server")
            connected = False
            break
        # Receive file size
        #file_size_bytes = conn.recv(1024)
        #file_size = int(file_size_bytes)

        # Receive start and end frames
        frames_info = conn.recv(1024).decode(FORMAT)
        start_frame, end_frame = map(int, frames_info.split(',')) # assigns the start and end frame values to theircorresponding variables

        # File reception and saving
        file_path = os.path.join(SAVE_PATH, file_name)
        with open(file_path, "wb") as file:
            file_data = b""
            while True:
                data = conn.recv(1024)
                if not data or b"<END>" in data:
                    file_data += data
                    break
                file_data += data
            file.write(file_data.replace(b"<END>", b""))  # Remove the <END> tag


        if conn.recv(1024) == b"<END>": # checks for end tag indicating completion of file transfer
            print(f"File {file_name} received successfully.")
        file.write(file_bytes) # writes the file bytes to the file variable
        
        #insert_into_project(file_name, client, frames_total, start_frame, end_frame)
        frames_total = 1 + (end_frame-start_frame) # gives us total frame value
        #insert_into_project(file_name,addr,frames_total, start_frame, end_frame

        # Blender rendering command
        blender_command = [
            "blender", "-b", file_path, 
            "-o", os.path.join(SAVE_PATH, "frame_#####"), 
            "-s", str(start_frame), "-e", str(end_frame), "-a"
        ]
        subprocess.run(blender_command) # essentialy creates a sort of bat file that is run
        
    conn.close() # closes the connection when !DISCONNECT message is sent
        

def start(): # code for server to start handling connections
    server.listen() # listening to connections
    print(f"[LISTENING] Server is listening on {server}")
    while True: # infinite loop for reasons
        conn, addr = server.accept() # code blocks and waits on .accept part of code until new connection occurs and then stores address and then store object allowing to send information back to connection
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}") # will tell us all the active client connections
#        if keyboard.keyboard.is_pressed('u'):
#            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
            
        

print("[STARTING] Server is starting...")
start()