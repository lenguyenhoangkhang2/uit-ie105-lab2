import socket
import ssl

PROXY_SERVER = "192.168.0.113"
SERVER = "192.168.0.111"
PORT = 5500
ADDR = (PROXY_SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

content = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
content.load_verify_locations("./example.crt")


def send(msg):
    sclient = content.wrap_socket(
        socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=SERVER
    )
    sclient.connect(ADDR)
    sclient.send(msg.encode(FORMAT))
    print(sclient.recv(2048).decode(FORMAT))
    sclient.close()


# message = input("What's your name?\n")

send("Hoang Khang")
send("Minh Duy")
send("Minh Thang")
send("My Trinh")

# disconnect to server
send(DISCONNECT_MESSAGE)
