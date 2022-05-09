import socket
import threading

HEADER = 10
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "BYE"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} has connected.")

    live = True
    while live:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length: # Check that message received is valid before decoding
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                live = False

            print(f"[{addr}] {msg}")
            conn.send("Message received".encode(FORMAT))

    print(f"[DISCONNECTING] {addr}")
    conn.close()


def start():
    server.listen()
    print(f"[SERVER OPEN] running on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Starting the server...")
start()