import random
import socket
import os
import customtkinter
import socket

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
def senderFunction(blenderFile, outputPath, startFrame, endFrame, client):
    file = open(blenderFile,"rb")
    file_size = os.path.getsize(blenderFile) # how many bytes the blender file has
    randomTail = random.randrange(1,99999,1)
    client.send(f"blendRender{randomTail}.blend".encode()) # will send file name with executable so the server knows its a blender file
    client.send(str(file_size).encode()) # typecasting the filesize variable as a string then encoding to send to server
    client.send(f"{startFrame},{endFrame}".encode()) # start and end frame are concatenated into a string
    data = file.read()
    client.sendall(data) # this is going to send the blender file to the server after giving it the initial
    client.send(b"<END>") # sending an end tag so the server knows when to stop listening