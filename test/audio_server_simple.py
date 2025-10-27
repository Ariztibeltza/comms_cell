import os
import socket
import threading
import pyaudio

# Audio constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Socket constants
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

## FUNCTIONS ##################################################################



## MAIN #######################################################################

p = pyaudio.PyAudio()
audio_stream  = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP,SERVER_PORT))
server.listen(1)

con,addr = server.accept()

try:
    while True:
        audio_data = audio_stream.read(CHUNK,exception_on_overflow=False)
        con.sendall(audio_data)
except KeyboardInterrupt:
    print("Stoped")
finally:
    con.close()
    server.close()
    audio_stream.stop_stream()
    audio_stream.close()
    p.terminate()
