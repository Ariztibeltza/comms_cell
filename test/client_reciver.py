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
BUTTON_PRESSED = False

## VARIABLES ##################################################################

key = b'ueoP3kd6cor-yviC8RwBgqqqkrLUQAhL85R4dQcfsyM='

## FUNCTIONS ##################################################################

## MAIN #######################################################################

p1 = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()
micro_stream = p1.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=AUDIO_CHUNK)
speaker_stream = p2.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      output=True,
                      frames_per_buffer=AUDIO_CHUNK)

fernet = Fernet(key)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP,SERVER_PORT))
print(f" ~ Connected to: {SERVER_IP}:{SERVER_PORT}")

try:
    while True:
        if BUTTON_PRESSED:
            #print("     ~ Recording")
            micro_data = micro_stream.read(AUDIO_CHUNK,
                                       exception_on_overflow=False)
            #print(sys.getsizeof(micro_data))
            enc_micro_data = fernet.encrypt(micro_data)
            #print(sys.getsizeof(enc_micro_data))
            client.sendall(enc_micro_data)
        else:
            print("     ~ Reciving")
            speaker_data = client.recv(SERVER_CHUNK)
            if not speaker_data:
                break
            try:
                enc_speaker_data = fernet.decrypt(speaker_data)
                speaker_stream.write(enc_speaker_data)
            except:
                print("Error in reception")
except OSError:                                      
    None
finally:
    client.close()
    micro_stream.stop_stream()
    speaker_stream.stop_stream()
    micro_stream.close()
    speaker_stream.close()
    p1.terminate()
    p2.terminate()