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

# FUNCTIONS ###################################################################

def start():
    while True:
        conn,addr = server.accept()
        # Create Thread



# MAIN ########################################################################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP,SERVER_PORT))
print(f" ~ Server: {SERVER_IP}:{SERVER_PORT}")
server.listen()

