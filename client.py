import socket
import pyaudio
from cryptography.fernet import Fernet
import asyncore
import collections

## CONSTANTS ##################################################################

# Audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
AUDIO_CHUNK = 512

# Server contants
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
SERVER_CHUNK = 2048

# Test
BUTTON_PRESSED = True

## VARIABLES ##################################################################

key = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='

## CLASSES ####################################################################

class Client(asyncore.dispatcher):
    def __init__(self,server_ip,server_port,key):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.outbox = collections.deque()
        self.microstream = pyaudio.PyAudio().open(format=FORMAT,
                                                channels=CHANNELS,
                                                rate=RATE,
                                                input=True,
                                                frames_per_buffer=AUDIO_CHUNK)
        self.audiostream = pyaudio.PyAudio().open(format=FORMAT,
                                                channels=CHANNELS,
                                                rate=RATE,
                                                output=True,
                                                frames_per_buffer=AUDIO_CHUNK)
        self.fernet = Fernet(key)
        self.connect((server_ip,server_port))
        print(f"[CNT] @ {server_ip}:{server_port}")

    def say(self):
        mssg = self.microstream.read(AUDIO_CHUNK,
                                    exception_on_overflow=False)
        if mssg!=None:
            self.outbox.append(mssg)
    
    def handle_write(self):
        if not self.outbox:
            return
        mssg = self.outbox.popleft()
        self.send(mssg)
    
    def handle_read(self):
        mssg = self.recv(SERVER_CHUNK)
        print(mssg)

## FUNCTIONS ##################################################################

## MAIN #######################################################################
client = Client(SERVER_IP,SERVER_PORT,key)

while True:
    if BUTTON_PRESSED:
        client.say()