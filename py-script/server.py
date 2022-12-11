import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8002))
sock.listen(5)
M = 1 <<  20
while True:
    connection, address = sock.accept()
    buf = connection.recv(M).decode()
    print(buf)
    #connection.send("please go out!".encode())
    connection.close()
