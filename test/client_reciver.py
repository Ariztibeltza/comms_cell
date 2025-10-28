import socket
import pyaudio
import keyboard

# Audio constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Server contants
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
CHUNK = 1024

# Test constants
BUTTON_PRESSED = False

## FUNCTIONS ##################################################################

## MAIN #######################################################################

p1 = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()
micro_stream = p1.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)
speaker_stream = p2.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      output=True,
                      frames_per_buffer=CHUNK)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP,SERVER_PORT))
print(f" ~ Connected to: {SERVER_IP}:{SERVER_PORT}")

try:
    while True:
        if BUTTON_PRESSED:
            #print("     ~ Recording")
            audio_data = micro_stream.read(CHUNK,
                                       exception_on_overflow=False)
            client.sendall(audio_data)
        else:
            print("     ~ Reciving")
            data = client.recv(CHUNK)
            if not data:
                break
            speaker_stream.write(data)
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