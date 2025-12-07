import socket
import pyaudio
from cryptography.fernet import Fernet
import sys
import threading

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

class Client(socket.socket):

    def __init__(self,addr,port,key):
        super().__init__(socket.AF_INET,socket.SOCK_STREAM)
        self.connect((addr,port))
        self.log('CLN', f'Connected to {addr}:{port}')
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
        self.b_pressed = False
        self.interlock = False
        threading.Thread(target=self.input,args=(),daemon=True).start()
        threading.Thread(target=self.output,args=()).start()
        
    
    def log(self,code,txt):
        print(f"[{code}] {txt}")

    def input(self):
        while True:
            data = self.recv(self.server_chunk)
            #if sys.getsizeof(data)<500:
                #self.interlock = True
                #print(key)
                #self.fernet.decrypt(data)
                #self.key = data
                #self.fernet = Fernet(key)
                #self.interlock = False
            if not data:
                break
            if not self.b_pressed:
                try:
                    dec_data = self.fernet.decrypt(data)
                    self.audiostream.write(dec_data,
                                           exception_on_underflow=False)
                except:
                    self.log("ERR", "Error decrypting")

    def output(self):
        while True:
            if self.b_pressed and not self.interlock:
                try:
                    m_data = self.microstream.read(self.audio_chunk,
                                                   exception_on_overflow=False)
                    enc_data = self.fernet.encrypt(m_data)
                    self.send(enc_data)
                except:
                    self.log("ERR", "Error sending data")

## FUNCTIONS ##################################################################

def main():
    client = Client(addr=SERVER_IP,port=SERVER_PORT,key = key)

## MAIN #######################################################################

main()