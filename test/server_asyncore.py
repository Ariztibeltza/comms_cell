import os
import socket
import json
from cryptography.fernet import Fernet
import asyncore
import collections


## CONSTANTS ##################################################################

# Server
SERVER_IP = "127.0.0.1"
#SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
SERVER_CHUNK = 2048
CLIENT_LIST = []
CLIENT_DICT = {}

## VARIABLES ##################################################################

# Crypto
key = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='

## CLASSES ####################################################################

class remote_client(asyncore.dispatcher):
    def __init__(self,host,socket,addr):
        asyncore.dispatcher.__init__(self,socket)
        self.host = host
        self.outbox = collections.deque()
    
    def say(self,mssg):
        self.outbox.append(mssg)
    
    def handle_read(self):
        mssg = self.recv(SERVER_CHUNK)
        self.host.broadcast(mssg)
    
    def handle_write(self):
        if not self.outbox:
            return
        mssg = self.outbox.popleft()
        self.send(mssg)


class server (asyncore.dispatcher):
    def __init__(self,addr,port,accptd_ip_list):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((addr,port))
        self.listen(10)
        self.ip_list = accptd_ip_list
        self.client_list = []
        print(f"[SRV] @ {addr}:{port}")
    
    def handle_accept(self):
        socket,addr = self.accept()
        print(f"[CNr] {socket.getsockname()[0]}")
        if socket.getsockname()[0] in self.ip_list:
            self.client_list.append(remote_client(self,socket,addr))
            print(f"[CNA] {socket.getsockname()[0]}")
        else:
            print(f"[CNR] {socket.getsockname()[0]}")
    
    def handle_read(self):
        print(f"Received mssg")
    
    def broadcast(self,mssg):
        print(f"Broadcasting")
        for client in self.client_list:
            client.say(mssg)

## FUNCTIONS ##################################################################

## MAIN #######################################################################

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

server(addr=SERVER_IP,
       port=SERVER_PORT,
       accptd_ip_list=d["client_ip"])
asyncore.loop()