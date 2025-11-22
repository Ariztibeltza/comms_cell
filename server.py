import os
import select
import json
from cryptography.fernet import Fernet
import socketserver
import queue
import pickle


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

class CustomServer(socketserver.ThreadingTCPServer):
    def __init__(self,addr,accptd_ip_list,request_handler_class):
        super().__init__(server_address=addr,
                         RequestHandlerClass=request_handler_class)
        self.accptd_ip_list = accptd_ip_list
        self.clients = set()
        print(f"[SRV] @ {addr}")
    
    def add_client(self,client):
        # Ensure the client is in the range we are willing to get
        self.log("CLr",f"{client}")
        self.clients.add(client)
    
    def broadcast(self,source,data):
        for client in tuple(self.clients):
            if client is not source:
                #print("~ Writing in buffer")
                #client.schedule(data)
                client.request.sendall(data)

    def remove_client(self,client):
        self.clients.remove(client)

    def log(self,code,txt):
        print(f"[{code}] {txt}")

class CustomHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.server.add_client(self)
        self.buffer = queue.Queue()
    
    def handle(self):
        try:
            while True:
                data = self.request.recv(2048)     #SERVER_CHUNK
                if data:
                    self.server.broadcast(self,data)
                #self.empty_buffers()
        except (ConnectionResetError, EOFError):
            print("[ERR]")
            pass
    
    #def empty_buffers(self):
        #print(self,"-",self.buffer.empty())
        #while not self.buffer.empty():
            #print(" ~ Sending data")
            #self.request.sendall(self.buffer.get())
    
    #def schedule(self,data):
        #print("~ Writing in buffer")
        #self.buffer.put(data)

    def finish(self):
        self.server.remove_client(self)
        self.request.close()
        #super().finish()

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
                          request_handler_class=CustomHandler)
    
    server.serve_forever()

## MAIN #######################################################################

main(key)