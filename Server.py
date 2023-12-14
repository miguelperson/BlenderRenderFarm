import socket
#import Client # allos us to use functions created within the gui code
import os # imports os handling library
import threading
# server side implementation of socket 
SERVER = socket.gethostbyname(socket.gethostname()) # gets IP address of server node
port = 5050 # port 8080 is apparently for HTTPs communications so will play it safe and not run on that port here
ADDR = (SERVER,port)
HEADER = 64 # will be the header for the data we want to send
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create sockets, AF INET is the socket type of family which is INET
server.bind(ADDR)


def handle_client(conn, addr): # handles communication between client and server, will use mutithreading
    print(f"[NEW CONNECTION] {addr} conneced.") # tells us who connected, connections will be running concurrently
    connected = True 
    while connected: #waiting to recieve information from client
        msg_length = conn.recv(HEADER).decode(FORMAT) # inputs how many bytes we need to recieve, conn.recieve is a blocking code so it will wait until something is sent, byte to string
        if msg_length: # detecting when the client sends something
            # this is a block just because the first reply from connection is essnetially blank so we want to ensure that e do the other stuff as long as there is stuff in the 
            msg_length = int(msg_length) # integer of total bytes we're going to be recieving
            msg = conn.recv(msg_length).decode(FORMAT) # msg now holds the 'message' holding all the contents from the client
            print(f"[{addr}] {msg}")
            done = False
            while not done:            
                data = client.recv(1024)
                file_bytes = b""
                if file_bytes[-5:] == b"<END>":
                    done = True
                    
                else:
                    file_bytes += data
            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            conn.send(f"message recieved".encode(FORMAT))
    conn.close() # closes the connection
        

def start(): # code for server to start handling connections
    server.listen() # listening to connections
    print(f"[LISTENING] Server is listening on {server}")
    while True: # infinite loop for reasons
        conn, addr = server.accept() # code blocks and waits on .accept part of code until new connection occurs and then stores address and then store object allowing to send information back to connection
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}") # will tell us all the active client connections
        

print("[STARTING] Server is starting...")
start()