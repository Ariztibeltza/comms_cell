import socket
import pyaudio
from cryptography.fernet import Fernet
import sys
import threading
import time

## CONSTANTS ##################################################################

# Audio constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
AUDIO_CHUNK = 512

# Server contants
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
SERVER_CHUNK = 2048

# Test constants
BUTTON_PRESSED = True

## VARIABLES ##################################################################

# Cryptography
key = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='

## CLASSES ####################################################################

class Client():

    def __init__(self,addr,port,key):
        self.addr = addr
        self.port = port
        self.input_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.output_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.audio_chunk = 512
        self.server_chunk = 2048
        self.microstream = pyaudio.PyAudio().open(format=self.format,
                      channels=self.channels,
                      rate=self.rate,
                      input=True,
                      frames_per_buffer=self.audio_chunk)
        self.audiostream = pyaudio.PyAudio().open(format=self.format,
                      channels=self.channels,
                      rate=self.rate,
                      output=True,
                      frames_per_buffer=self.audio_chunk)
        self.key = key
        self.fernet = Fernet(self.key)
        self.b_pressed = True
        self.interlock = False
        self.conn_sockets()        
        threading.Thread(target=self.input,args=(),daemon=True).start()
        threading.Thread(target=self.output,args=()).start()
        
    def conn_sockets(self):
        # Set-up the input socket
        try:
            self.input_socket.connect((self.addr,self.port))
            self.log('CLN', f'Connected to {self.addr}:{self.port}')
        except:
            self.log('ERR', f'Error in connection')
        time.sleep(1)
        try:
            self.output_socket.connect((self.addr,self.port))
            self.log('CLN', f'Connected to {self.addr}:{self.port}')
        except:
            self.log('ERR', f'Error in connection')

    def log(self,code,txt):
        print(f"[{code}] {txt}")

    def input(self):
        while True:
            data = self.input_socket.recv(self.server_chunk)
            #if sys.getsizeof(data)<500:
                #self.interlock = True
                #print(key)
                #self.fernet.decrypt(data)
                #self.key = data
                #self.fernet = Fernet(key)
                #self.interlock = False
            if not data:
                break
            elif not self.b_pressed and data:
                try:
                    dec_data = self.fernet.decrypt(data)
                    self.audiostream.write(dec_data,
                                           exception_on_underflow=False)
                except:
                    self.log("ERR", "Error decrypting")

    def output(self):
        while True:
            if self.b_pressed and not self.interlock:
                #try:
                    m_data = self.microstream.read(self.audio_chunk,
                                                   exception_on_overflow=False)
                    enc_data = self.fernet.encrypt(m_data)
                    self.output_socket.sendall(enc_data)
                #except Error:
                    #self.log("ERR", "Error sending data")

## FUNCTIONS ##################################################################

def main():
    client = Client(addr=SERVER_IP,port=SERVER_PORT,key = key)

## MAIN #######################################################################

main()