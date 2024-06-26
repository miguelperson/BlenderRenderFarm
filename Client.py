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
# ADDR = (HOST, PORT)
counter = 0  # will be used to keep track of the files sent

def connectionFunction(HOST, PORT, error_callback=None):
    try:
        ADDR = (HOST, PORT)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)  # Connect to the server
        client.sendall(b'client')
        print(f"Connected to {HOST} on {PORT}")
        return client
    except socket.error as e:
        print(f"Error connecting to {HOST} on {PORT}: {e}")
        if error_callback:
            error_callback()
        return  # Exit the function or handle the error as needed



def send_file_to_server(file_path, output_folder, start_frame, end_frame, client, username):
    try:    
        if not os.path.isfile(file_path):  # checks if file exists
            print(f"File not found: {file_path}")
            return  # Prepare file info (filename and filesize)
        filesize = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        file_info = f"{filename};{filesize};{start_frame};{end_frame};{username}"  # sends all the important information as one sort of byte stream
        # Send file info
        client.sendall(file_info.encode())

        # Wait for confirmation from the server
        confirmation = client.recv(1024).decode()
        if confirmation == "INFO_RECEIVED":  # if the recieved message is the confirmation message
            # Send the file
            with open(file_path, 'rb') as f:  # opens the file in read byte mode
                while True:
                    bytes_read = f.read(4096)  # sendn file as chunks so server can recieve in chunks as well
                    if not bytes_read:
                        break  # File transmitting is done
                    client.sendall(bytes_read)
        print(f"File {filename} has been sent.")

        zip_info = client.recv(1024).decode()
        zip_name, zip_size = zip_info.split(';')
        zip_name = os.path.basename(zip_name)
        zip_size = int(zip_size)
        client.send("INFO_RECEIVED".encode())
        zip_file_path = os.path.join(output_folder, zip_name)
        with open(zip_file_path, 'wb') as f:
            bytes_received = 0
            while bytes_received < zip_size:
                chunk = client.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)
            #client.send("INFO_RECEIVED".encode())
    finally:
        print(f"File {filename} has been received and saved.")


# following code will be for when server responds with the zip files storing the frames of the zip file thats recieved
def recieverFunction(client, outputFolder):
    zipFileName = client.recv(1028).decode()  # recieves file name
    zipFileSize = int(client.recv(1024)).decode()  # recieves the file size from the server

    recievedData = b""  # will store byte stream of the recieved data from the server
    while len(
            recievedData) < zipFileSize:  # loop continues while the recievedData vairable is smaller than actual data recieved
        chunk = client.recv(1024)
        if not chunk:
            break
        recievedData += chunk  # concatenates the chunk data to the end of recieved data, essentially putting the data we recieve at the end
    with open(zipFileName, 'wb') as f:  # save zip file
        f.write(recievedData)


def disconnectMessage(client):
    client.send('!DISCONNECT;;;'.encode())