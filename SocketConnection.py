import socket
import gui # allos us to use functions created within the gui code
import os # imports os handling library
import threading
# server side implementation of socket 
host = socket.gethostbyname(socket.gethostbyname) # gets IP address of server node
port = 5050 # port 8080 is apparently for HTTPs communications so will play it safe and not run on that port here

totalClient = int(input('Enter number of clients:'))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create sockets, AF INET is the socket type of family which is INET
server.bind((host,port)) # anything connecting to our IP and port is going right into the 'server' socket 
server.listen(totalClient) # has the socket listen for the total number of clients initially given.

def handle_client(conn, addr): # handles communication between client and server, will use mutithreading
    pass

def start(): # code for server to start handling connections
    server.listen() # listening to connections
    while True: # infinite loop for reasons
        conn, addr = server.accept() # code blocks and waits on .accept part of code until new connection occurs and then stores address and then store object allowing to send information back to connection
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}") # will tell us all the active client connections
        

print("[STARTING] Server is starting...")
start()