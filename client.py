import socket
import pyaudio
from cryptography.fernet import Fernet
import sys

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
        self.b_pressed = True
    
    def log(self,code,txt):
        print(f"[{code}] {txt}")

    def loop(self):
        while True:
            if self.b_pressed:
                try:
                    m_data = self.microstream.read(self.audio_chunk)
                    enc_data = self.fernet.encrypt(m_data)
                    self.sendall(enc_data)
                except:
                    self.feedback()
            else:
                data = self.recv(self.server_chunk)
                if not data:
                    break
                try:
                    dec_data = self.fernet.decrypt(data)
                    self.audiostream.write(dec_data)
                except:
                    self.log("ERR", "Error decrypting")

## FUNCTIONS ##################################################################

def main():
    client = Client(addr=SERVER_IP,port=SERVER_PORT,key = key)
    client.loop()

## MAIN #######################################################################

main()