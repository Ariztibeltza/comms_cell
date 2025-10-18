import socket
import json

file = open("rsrcs/keys.json")
client_dict = json.load(file)
client_list = []

server = socket.socket(socket.AF_BLUETOOTH,
                           socket.SOCK_STREAM,
                           socket.BTPROTO_RFCOMM)
channel=10
server.bind(("9c:29:76:03:c5:b8",channel))
server.listen(1)

(client,addr) = server.accept()

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        print(f"Message: {data.decode('utf-8')}")
except OSError:
    None

client.close()
server.close()



