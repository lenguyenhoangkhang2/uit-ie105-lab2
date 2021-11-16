import pdb
import socket
import sys
import threading

PROXY_SERVER = "192.168.0.113"
SERVER = "192.168.0.111"
PROXY_LISTENER_PORT = SERVER_LISTENER_PORT = 8080
BUFFER_SIZE = 2048

proxyServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxyServer.bind((PROXY_SERVER, PROXY_LISTENER_PORT))


def proxy_handle(client_conn, client_addr):
    # pdb.set_trace()
    print(f"[NEW CONNECTION] {client_addr}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"[CONNECT SERVER] {SERVER}:{SERVER_LISTENER_PORT}")
        sock.connect((SERVER, SERVER_LISTENER_PORT))

        while True:
            data = client_conn.recv(BUFFER_SIZE)

            if len(data):
                print(
                    f"[*] Request from {client_addr} to {(SERVER, SERVER_LISTENER_PORT)}"
                )
                sock.send(data)

                reply = sock.recv(BUFFER_SIZE)
                if len(reply):
                    print(
                        f"[*] Response from {(SERVER,SERVER_LISTENER_PORT)} to {client_addr}"
                    )
                    client_conn.send(reply)

            else:
                break

        print(f"[CLOSE CLIENT CONNECT] {client_addr}")
        print(f"[DISCONNECT SERVER] {SERVER}:{SERVER_LISTENER_PORT}")
        sock.close()
        client_conn.close()

    except socket.error as e:
        print(e)
        client_conn.close()
        sys.exit(1)


def start():
    proxyServer.listen()
    print(f"[*] Server started [{PROXY_SERVER}:{PROXY_LISTENER_PORT}]")

    while True:
        try:
            client_conn, client_addr = proxyServer.accept()
            thread = threading.Thread(
                daemon=True, target=proxy_handle, args=(client_conn, client_addr)
            )
            thread.start()
            print(f"[active connections] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            proxyServer.close()
            print("\n[*] Graceful Shutdown")
            sys.exit(1)


start()
