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
        return client
    except socket.error as e:
        print(f"Error connecting to {SERVER} on {PORT}: {e}")
        if error_callback:
            error_callback()
        return  # Exit the function or handle the error as needed
    

def senderFunction(blenderFile, outputPath, startFrame, endFrame, client, username):
    file = open(blenderFile,"rb")
    file_size = os.path.getsize(blenderFile) # how many bytes the blender file has
    randomTail = random.randrange(1,99999,1)
    
    client.send(f"blendRender{randomTail}.blend".encode()) # will send file name with executable so the server knows its a blender file
    #client.send(str(file_size).encode()) # typecasting the filesize variable as a string then encoding to send to server
    client.send(f"{startFrame},{endFrame}".encode(FORMAT)) # start and end frame are concatenated into a string
    
    data = file.read()
    client.sendall(data) # this is going to send the blender file to the server after giving it the initial
    client.send(b"<END>") # end tag is so the server knows when the end of the file is


# following code will be for when server responds with the zip files storing the frames of the zip file thats recieved
def recieverFunction(client, outputFolder):
    zipFileName = client.recv(1028).decode() # recieves file name
    zipFileSize = int(client.recv(1024)).decode() # recieves the file size from the server

    recievedData = b"" # will store byte stream of the recieved data from the server
    while len(recievedData) < zipFileSize: # loop continues while the recievedData vairable is smaller than actual data recieved
        chunk = client.recv(1024)
        if not chunk:
            break
        recievedData += chunk #concatenates the chunk data to the end of recieved data, essentially putting the data we recieve at the end
    with open(zipFileName, 'wb') as f: # save zip file
        f.write(recievedData)
        
def disconnectMessage(client):
    client.send('!DISCONNECT'.encode())