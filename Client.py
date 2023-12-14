import socket
import os


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.99.139" # this would need to be updated if the server IP changes
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR) # this connects to the server

def send(msg):
    message = msg.encode(FORMAT) # message is the file we want to send, encoding it to be good for sending
    msg_length = len(message) # get the length (in bytes) of the message
    send_length = str(msg_length).encode(FORMAT) # will first send the length of the 'message' as a header
    # need to make header message 64 bytes long so will add 'padding' to message just in case it doesn't take the full 64 bytes 
    send_length += b' '* (HEADER - len(send_length)) # b -> byte representation of the blank space
    client.send(send_length) # sending the header
    client.send(message) # then we send the message
    print(client.recv(2048).decode(FORMAT)) # prints the message recieved from the server to the terminal, put 2048 because server responses are known to be short
    
def send_file(file_location):
    file = open(file_location,"rb") # rb -> reading byte mode
    file_size = os.path.getsize(file_location) # will give us the file 
    send_size = str(file_size).encode(FORMAT)
    send_length += b' '* (HEADER - len(send_length)) # b -> byte representation of the blank space
    client.send("temp_file_name.png".encode()) # sending file name, will want to make a random generator here though
    client.send(send_size) # sends the header with the file size
    data = file.read()
    client.sendall(data) # sends all the data from the file

def disconnect():
    send("!DISCONNECT")
    
# send("recieved_image.png".encode()) # gets file name
# send(str(file_size).encode()) # this should be the file size
# send("!DISCONNECT")