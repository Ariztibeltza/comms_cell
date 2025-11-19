import os
import socket
import threading
import json
from cryptography.fernet import Fernet
import random
import queue

# CONSTANTS ###################################################################

# Server
SERVER_IP = "127.0.0.1"
#SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
SERVER_CHUNK = 2048
CLIENT_LIST = []
CLIENT_DICT = {}

# VARIABLES ###################################################################

# Data
data_queue = queue.Queue(100)

# Cryptography
key = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='
frameCount = random.randint(200,1000)
i = 0

# FUNCTIONS ###################################################################

def client_handler(conn,addr,data_queue):
    connected = True
    try:
        while connected:
            client_data = conn.recv(SERVER_CHUNK)
            if client_data:
                print("Client data")
                data_queue.put([conn,client_data])
                #print(len(CLIENT_DICT.keys()))
                #for client in CLIENT_DICT.keys():
                    #if str(conn)!=CLIENT_DICT[client]:
                        #CLIENT_DICT[client][0].sendall(client_data)
    except:
        connected = False
        print(f"[DCN] {conn.getsockname()[0]}")
        conn.close()

def start(ip_list,data_queue):
    while True:
        conn,addr = server.accept()
        print(f"[CNr] {conn.getsockname()[0]}")
        if conn.getsockname()[0] in ip_list:
            print(f"[CNA] {conn.getsockname()[0]}")
            CLIENT_DICT[str(conn)]=[conn,addr]
            thread = threading.Thread(target=client_handler,args=(conn,addr,data_queue))
            thread.start()
        else:
            print(f"[CMR] {conn.getsockname()[0]}")
        
        if data_queue.empty()!=False:
            client_data = data_queue.get()
            print("Data")
            #for client in CLIENT_DICT.keys():
            #    if 


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
start(ip_list=d["client_ip"],data_queue=data_queue)

