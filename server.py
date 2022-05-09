import socket
import threading

HEADER = 10
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "END"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

usernames = ["Amaar", "Nirmal", "Robyn", "Patrick"]
blacklist = []


def get_message(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length: # Check that message received is valid before decoding
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} has connected.")
    live = True
    while live:
        send_to_client(conn, "Please authenticate with AUTH <username>")
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length: # Check that message received is valid before decoding
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msg = msg.strip()
            user = msg[4:].strip()
            if msg[:4] == "AUTH" and user in usernames:
                console_message(addr, msg)
                send_to_client(conn, f"Successfully authenticated, hello {user}!")
                live = False

    print(f"[DISCONNECTING] {addr}")
    conn.close()


def console_message(addr, msg):
    print(f"[{addr}] {msg}")


def send_to_client(conn, msg):
    conn.send(msg.encode(FORMAT))


def start():
    server.listen()
    print(f"[SERVER OPEN] running on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def __main__():
    print("[STARTING] Starting the server...")
    start()


__main__()