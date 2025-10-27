import socket
import pyaudio

# Audio constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Server data
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

## MAIN #######################################################################

p = pyaudio.PyAudio()
audio_stream  = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       output=True,
                       frames_per_buffer=CHUNK)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP,SERVER_PORT))

try:
    while True:
        data = client.recv(CHUNK)
        if not data:
            break
        audio_stream.write(data)
except KeyboardInterrupt:
    print("Stop")
finally:
    client.close()
    audio_stream.stop_stream()
    audio_stream.close()
    audio_stream.close()
    p.terminate
