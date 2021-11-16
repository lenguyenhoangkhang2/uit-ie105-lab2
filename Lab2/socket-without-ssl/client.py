import socket

PROXY_SERVER = "192.168.0.113"
PORT = 8080
ADDR = (PROXY_SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    client.send(msg.encode(FORMAT))
    print(client.recv(2048).decode(FORMAT))


# message = input("What's your name?\n")

send("Hoang Khang")
send("Minh Duy")
send("Minh Thang")
send("My Trinh")

# disconnect to server
client.close()
