import os
import socket
import threading
import pyaudio

# CONSTANTS ###################################################################

# Server
SERVER_IP = "127.0.0.1"
#SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
CHUNK = 1024
CLIENT_LIST = []

# FUNCTIONS ###################################################################

def client_handler(conn,addr):
    try:
        while True:
            client_data = conn.recv(CHUNK)
            if client_data:
                #print(f"    ~ Data from: {conn},{addr}")
                for client in CLIENT_LIST:
                    if conn!=client[0]:
                        client[0].sendall(client_data)
                        print(f"    ~ Data sent to {client[0]},{client[1]}")
    except:
        None

def start():
    while True:
        conn,addr = server.accept()
        print(f"     ~ Connection accepted")
        CLIENT_LIST.append([conn,addr])
        thread = threading.Thread(target=client_handler,args=(conn,addr))
        thread.start()


# MAIN ########################################################################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP,SERVER_PORT))
print(f" ~ Server: {SERVER_IP}:{SERVER_PORT}")
server.listen()
start()

