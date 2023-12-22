import socket
#import Client # allos us to use functions created within the gui code
import os
from sqlite3 import connect # imports os handling library
import threading
import tqdm
from manipulateDB import *

# server side implementation of socket 
SERVER = socket.gethostbyname(socket.gethostname()) # gets IP address of server node
port = 5050 # port 8080 is apparently for HTTPs communications so will play it safe and not run on that port here
ADDR = (SERVER,port)
HEADER = 1024 # will be the header for the data we want to send
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SAVE_PATH = "C:\Users\Miguel Baca\Pictures\BlenderRenderFIles"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create sockets, AF INET is the socket type of family which is INET
server.bind(ADDR)


def handle_client(conn, addr): # handles communication between client and server, will use mutithreading
    print(f"[NEW CONNECTION] {addr} connected.") # tells us who connected, connections will be running concurrently
    connected = True 
    while connected: #waiting to recieve information from client
        file_name = conn.recv(HEADER).decode() # the .recv() is a blocking code, will also recieve the file name first
        if file_name == DISCONNECT_MESSAGE:
            connected = False
            break
        print(file_name) # just pringing the name to console
        file_size = conn.recv(1024).decode()
        print(file_size) # prints file size to the console 
        file = open(file_name, "wb") # kinda creating a file with the name file_name, oging to concatenate bytes to it now
        file_bytes = b""
        progress = tdqm.tdqm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size)) # creating progress bar
        done = False
        while not done:
            data = conn.recv(1024) # transmits data in chunks to make it more efficient
            if file_bytes[-5:] == b"<END>":
                done = True
            else:
                file_bytes += data
            progress.update(1024) # updates the progress bar
        file.write(file_bytes) # writes the file bytes to the file variable    
        # add line to execute sql command to insert into project table || insert_into_project(project_name, client, frames_total, start_frame, end_frame)
        frames_total = 1 + (end_frame-start_frame) # gives us total frame value
        insert_into_project(file_name,addr,frames_total, start_frame, end_frame)
    conn.close() # closes the connection
        

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