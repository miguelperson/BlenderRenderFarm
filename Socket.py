import socket

host = '192.168.99.50'
port = 8080
totalClient = int(input('Enter number of clients:'))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host,port))
sock.listen(totalClient)

def connection():
    print('placeholder')
    