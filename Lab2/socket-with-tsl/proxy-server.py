import socket
import sys
import threading

PROXY_SERVER = "192.168.0.113"
SERVER = "192.168.0.111"
PROXY_LISTENER_PORT = SERVER_LISTENER_PORT = 5500
BUFFER_SIZE = 2048

proxyServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxyServer.bind((PROXY_SERVER, PROXY_LISTENER_PORT))


def proxy_handle(conn, data, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER, SERVER_LISTENER_PORT))
        sock.send(data)

        while True:
            reply = sock.recv(BUFFER_SIZE)
            if len(reply):
                conn.send(reply)

                print(f"[*] Request Done From: {addr}")
            else:
                break

        conn.close()
        sock.close()
    except Exception:
        sock.close()
        conn.close()
        sys.exit(1)


def start():
    proxyServer.listen()
    print(f"[*] Server started [{PROXY_SERVER}:{PROXY_LISTENER_PORT}]")

    while True:
        try:
            conn, addr = proxyServer.accept()
            data = conn.recv(BUFFER_SIZE)
            thread = threading.Thread(
                daemon=True, target=proxy_handle, args=(conn, data, addr)
            )
            thread.start()
            print(f"[active connections] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            proxyServer.close()
            print("\n[*] Graceful Shutdown")
            sys.exit(1)


start()
