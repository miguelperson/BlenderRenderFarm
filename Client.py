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
client_IP = socket.gethostbyname(socket.gethostname())

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
    file_size = os.path.getsize(file_location) # will give us the file size
    send_length = str(file_size).encode(FORMAT) # stores length as a string for some reason
    client.send("[placeholder].blend".encode())
    client.send(str(file_size).encode())
    data = file.read()
    client.sendall(data) # works on sending end, reciever will know file size but doesn't immediately know it
    client.send(b"<END>") # end tag will indicate end of sending file

def disconnect():
    send("!DISCONNECT")
    
# send(str(client_IP)) # sends the IP to the server
# send("recieved_image.png".encode()) # gets file name
# send(str(file_size).encode()) # this should be the file size
# send("!DISCONNECT")