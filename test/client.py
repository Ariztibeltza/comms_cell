import socket
import cryptography

client = socket.socket(socket.AF_BLUETOOTH,
                           socket.SOCK_STREAM,
                           socket.BTPROTO_RFCOMM)
channel=10
client.connect(("9c:29:76:03:c5:b8",channel))


try:
    while True:
        mssg = input("Message: ")
        client.send(mssg.encode("utf-8"))
except OSError:
    None

client.close()