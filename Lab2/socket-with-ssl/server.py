import socket
import sys
import threading
import ssl

SERVER = "192.168.0.111"
PORT = 5500
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
BUFFER_SIZE = 2048

content = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
content.load_cert_chain("./example.crt", "./example.key")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        msg = conn.recv(BUFFER_SIZE).decode(FORMAT)
        if len(msg):
            if msg == DISCONNECT_MESSAGE:
                print(f"[{addr}] Disconnected XXX")
                break

            print(f"[{addr}] Send message: {msg}")
            conn.send(f"Hello {msg}!".encode(FORMAT))

    conn.close()


def start():
    server.listen()
    sserver = content.wrap_socket(server, server_side=True)
    print(f"[LISTENING] server is listening on {SERVER}/{PORT}")
    while True:
        try:
            conn, addr = sserver.accept()
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
