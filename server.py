import os
import json
from cryptography.fernet import Fernet
import socketserver
import random
import sys

## CONSTANTS ##################################################################

# Server
SERVER_IP = "127.0.0.1"
#SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
SERVER_CHUNK = 2048
CLIENT_LIST = []
CLIENT_DICT = {}

## VARIABLES ##################################################################

# Cryptography
key = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='

## CLASSES ####################################################################

class CustomServer(socketserver.ThreadingTCPServer):
    def __init__(self,addr,accptd_ip_list,request_handler_class,key):
        super().__init__(server_address=addr,
                         RequestHandlerClass=request_handler_class)
        self.accptd_ip_list = accptd_ip_list
        self.clients = set()
        self.key = key
        self.cycle_threshold = random.randint(2000,5000)
        self.cycles = 0
        self.fernet = Fernet(key)
        print(f"[SRV] @ {addr}")
    
    def add_client(self,client):
        # Ensure the client is in the range we are willing to get
        self.log("CLr",f"{client.request.getsockname()[0]}")
        if client.request.getsockname()[0] in self.accptd_ip_list:
            self.log("CLA","Client accepted")
            self.clients.add(client)
        else:
            self.log("CLR","Client accepted")
    
    def broadcast(self,source,data):
        for client in tuple(self.clients):
            if client is not source:
                client.request.sendall(data)
        #self.cycles +=1
        #if self.cycles >= self.cycle_threshold:
            #self.reencrypt()
            #for client in tuple(self.clients):
                #print("~ Sending")
                #print(sys.getsizeof(data))
                #client.request.send(data)

    def remove_client(self,client):
        self.clients.remove(client)

    def log(self,code,txt):
        print(f"[{code}] {txt}")

    def reencrypt(self):
        self.cycle_threshold = random.randint(5000,7000)
        self.cycles = 0
        self.log("ENC","Reencryption")
        key = Fernet.generate_key()
        mssg = self.fernet.encrypt(key)
        self.key = key
        self.fernet = Fernet(self.key)

class CustomHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.server.add_client(self)
    
    def handle(self):
        try:
            while True:
                data = self.request.recv(2048)     #SERVER_CHUNK
                if data:
                    self.server.broadcast(self,data)
        except (ConnectionResetError, EOFError):
            print("[CLD] Client disconnected")
            pass

    def finish(self):
        self.server.remove_client(self)
        self.request.close()

## FUNCTIONS ##################################################################

def main(key):
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

    ip_list = d["client_ip"]

    server = CustomServer(addr=(SERVER_IP,SERVER_PORT),
                          accptd_ip_list=ip_list,
                          request_handler_class=CustomHandler,
                          key = key)
    
    server.serve_forever()

## MAIN #######################################################################

main(key)