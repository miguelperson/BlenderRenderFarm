import socket
import gui # allos us to use functions created within the gui code
# server side implementation of socket code
host = '192.168.99.50'
port = 8080
totalClient = int(input('Enter number of clients:'))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create 
sock.bind((host,port))
sock.listen(totalClient) # has the socket listen for the total number of clients initially given.

connections = [] # array of connection objects 

print('time to initializa these mother fuckin connections')

for i in range(totalClient): # connecting ricardos computer to the server
    conn = sock.accept() # accepts socket connection with clients
    connections.apend(conn) # appending connection to array for the sake of storage and shit
    print('connected with the client', i+1) # console confirmation of the client being conneced (Ricardo)

fileno = 0
idx = 0
for conn in connections:
    # recieving file data
    idx += 1
    data = conn[0].recv(1024).decode
    if not data: 
        continue
    filename = 'output'+str(fileno)+'.txt'
    fileno = fileno+1
    

# creating a new file at server end and writig the data
def connection():
    print('placeholder')
