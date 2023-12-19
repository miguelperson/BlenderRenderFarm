import socket
import os
import threading

SERVER = socket.gethostbyname(socket.gethostname())
port = 5050
ADDR = (SERVER, port)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Specify the predetermined file path where you want to save the received files
SAVE_PATH = "C:\\Users\\Miguel Baca\\Pictures\\BlenderRenderFIles"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # Save the file in the predetermined folder
            file_path = os.path.join(SAVE_PATH, msg)
            with open(file_path, "wb") as file:
                while True:
                    file_data = conn.recv(1024)
                    if not file_data:
                        break
                    file.write(file_data)

            print(f"[{addr}] File saved at: {file_path}")
            
            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            conn.send("Message received".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {server}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] Server is starting...")
start()
