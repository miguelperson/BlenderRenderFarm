import socket
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
    

def connection():
    print('placeholder')




# THIS IS AN EXAMPLE PUSH PLEASE DISREGARD