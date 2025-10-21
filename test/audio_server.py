import socket
import threading
import pyaudio
import cryptography

## INFO #######################################################################

# https://people.csail.mit.edu/hubert/pyaudio/docs
# https://gist.github.com/kevindoran/5428390
# https://www.geeksforgeeks.org/python/multithreading-python-set-1

###############################################################################

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_TIME = 5
OUT_FILE = "output.wav"

IP = socket.gethostbyname(socket.gethostname())
PORT = 10000
BACKLOG = 5
SIZE = CHUNK

server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
print(IP,":",PORT)
server.bind((IP,PORT))
server.listen(BACKLOG)

micro_audio = pyaudio.PyAudio()
micro_stream = micro_audio.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

speaker_audio = pyaudio.PyAudio()
speaker_audio = speaker_audio.open(fromat=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   output=True,
                                   frames_per_buffer=CHUNK)

def handle_client(conn,addr):
    connected = True
    while connected:
        client_data = conn.recv(SIZE)
        

def start():
    while True:
        data = micro_stream.read(CHUNK)
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        try:
            while True:
                client_data = server.recv(SIZE)
                if client_data:
                    print('Sending data back')
                    # Reproducir el audio
                else:
                    print('No data from ', addr)
                conn.sendall(data)
        except:
            conn.close()

start()

