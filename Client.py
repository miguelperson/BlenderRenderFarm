import socket
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.99.139" # this would need to be updated if the server IP changes
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT) # message is the file we want to send
    msg_length = len(message) # get the length (in bytes) of the message
    send_length = str(msg_length).encode(FORMAT) # will first send the length of the 'message' as a header
    # need to make header message 64 bytes long so will add 'padding' to message just in case it doesn't take the full 64 bytes 
    send_length += b' '* (HEADER - len(send_length)) # b -> byte representation of the blank space
    client.send(send_length) # sending the header
    client.send(message) # then we send the message
    
send("hello kindman")