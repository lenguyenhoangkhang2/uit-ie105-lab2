import socket
import sys
import threading

SERVER = "192.168.0.111"
PORT = 8080
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
BUFFER_SIZE = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        msg = conn.recv(BUFFER_SIZE).decode(FORMAT)
        if len(msg):
            print(f"[{addr}] Send message: {msg}")
            conn.send(f"Hello {msg}!".encode(FORMAT))
        else:
            break

    print(f"[CLOSE CONNECT] {addr}")
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}/{PORT}")
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(
                daemon=True, target=handle_client, args=(conn, addr)
            )
            thread.start()
            print(f"[active connections] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            server.close()
            print("\n[*] Graceful Shutdown")
            sys.exit(1)


start()
