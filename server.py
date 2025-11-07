import os
import socket
import threading
import json
from cryptography.fernet import Fernet
import random

# CONSTANTS ###################################################################

# Server
SERVER_IP = "127.0.0.1"
#SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
SERVER_CHUNK = 2048
CLIENT_LIST = []

# VARIABLES ###################################################################

# Cryptography
key = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='
frameCount = random.randint(200,1000)

# FUNCTIONS ###################################################################

def client_handler(conn,addr):
    try:
        while True:
            client_data = conn.recv(SERVER_CHUNK)
            if client_data:
                #print(f"    ~ Data from: {conn},{addr}")
                #enc_data = fernet.encrypt(client_data)
                for client in CLIENT_LIST:
                    if conn!=client[0]:
                        client[0].sendall(client_data)
                        print(f"    ~ Data sent to {client[0]},{client[1]}")
    except:
        None

def start(ip_list):
    while True:
        conn,addr = server.accept()
        print(f"     ~ Connection request: {conn.getsockname()[0]}")
        if conn.getsockname()[0] in ip_list:
            print(f"     ~ Connection accepted: {conn.getsockname()[0]}")
            CLIENT_LIST.append([conn,addr])
            thread = threading.Thread(target=client_handler,args=(conn,addr))
            thread.start()
        else:
            print(f"     ~ Connection refused: {conn.getsockname()[0]}")
        


# MAIN ########################################################################
fernet = Fernet(key)

file = open("./rsrcs/enc.json","rb")
enc = file.read()
file.close()
decr = fernet.decrypt(enc)

tmpfile = open("./rsrcs/tmp.json","wb")
tmpfile.write(decr)
tmpfile.close()
tmpfile = open("./rsrcs/tmp.json","rb")
d = json.load(tmpfile)
tmpfile.close()
os.remove(path="./rsrcs/tmp.json")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP,SERVER_PORT))
print(f" ~ Server: {SERVER_IP}:{SERVER_PORT}")
server.listen()
start(ip_list=d["client_ip"])

