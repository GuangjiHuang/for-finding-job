import socket
import time

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    M = 1 << 10
    print(M)
    sock.connect(("localhost", 8002))
    time.sleep(1)
    data = input("sending Message: ").encode()
    sock.send(data)
    print(sock.recv(M).decode())
    sock.close()
