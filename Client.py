from http import client
import random
import socket
import os
import customtkinter
import socket

FORMAT = 'utf-8'
HEADER = 64

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# HOST = '192.168.99.113'  # Server's IP  # Update with the actual server IP ===============================
ADDR = (SERVER, PORT)
counter = 0  # will be used to keep track of the files sent

def connectionFunction(HOST, PORT,error_callback=None):
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
    

def send_file_to_server(host, port, file_path):
    if not os.path.isfile(file_path): # checks if file exists
        print(f"File not found: {file_path}")
        return    # Prepare file info (filename and filesize)
    filesize = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    file_info = f"{filename};{filesize}"
    # Send file info
    client.sendall(file_info.encode())

    # Wait for confirmation from the server
    confirmation = s.recv(1024).decode()
    if confirmation == "INFO_RECEIVED":
        # Send the file
        with open(file_path, 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break  # File transmitting is done
                s.sendall(bytes_read)

    print(f"File {filename} has been sent.")



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