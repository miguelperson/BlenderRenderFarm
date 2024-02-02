import random
import socket
import os
import socket
# import ClientCustomGUI # this will be so we can pass error functions to the front end if needed

def connectionFunction(error_callback=None):
    HEADER = 64
    PORT = 5050
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    SERVER = "192.168.99.139"  # Update with the actual server IP
    ADDR = (SERVER, PORT)
    counter = 0  # will be used to keep track of the files sent

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)  # this connects to the server
        client_IP = socket.gethostbyname(socket.gethostname())
        print(f"Connected to {SERVER} on {PORT}")
    except socket.error as e:
        print(f"Error connecting to {SERVER} on {PORT}: {e}")
        if error_callback:
            error_callback()
        return  # Exit the function or handle the error as needed

def sendFile(file_path, firstFrame, lastFrame):
    print('placeholder for send function')
