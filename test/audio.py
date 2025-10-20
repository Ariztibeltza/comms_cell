import socket
import threading
import pyaudio
import cryptography

## INFO #######################################################################

# https://people.csail.mit.edu/hubert/pyaudio/docs
# https://gist.github.com/kevindoran/5428390

###############################################################################

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_TIME = 5
OUT_FILE = "output.wav"

HOST_MAC = "9c:29:76:c5:b8"
HOST_PORT = 10
SERVER_MAC = ""
SERVER_PORT = 11
BACKLOG = 1
SIZE = 1024

server = socket.socket(socket.AF_BLUETOOTH,
                       socket.SOCK_STREAM,
                       socket.BTPROTO_RFCOMM)

client = socket.socket(socket.AF_BLUETOOTH,
                       socket.SOCK_STREAM,
                       socket.BTPROTO_RFCOMM)
client.connect()

micro_audio = pyaudio.PyAudio()
micro_stream = micro_audio.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

while True:
    data = micro_stream.read(CHUNK)
    client.send(data)