import socket

host = '192.168.99.50'
port = 8080
totalClient = int(input('Enter number of clients:'))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create 
sock.bind((host,port))
sock.listen(totalClient) # has the socket listen for the total number of clients initially given.

connection = [] # array of connection objects 

print('time to initializa these mother fuckin connections')

for i in range(totalClient):
    conn = sock.accept() # accepts socket connection with clients
    connection.apend(conn) # appending connection to array for the sake of storage and shit

def connection():
    print('placeholder')
