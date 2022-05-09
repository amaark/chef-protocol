import socket

HEADER = 10
PORT = 5050
SERVER = "192.168.0.16" # Change this to server IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "END"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    sock.send(send_length)
    sock.send(message)
    print(sock.recv(2048).decode(FORMAT))

def __main__():
    sock.connect(ADDR)
    live = True
    while live == True:
        send(input())


__main__()
