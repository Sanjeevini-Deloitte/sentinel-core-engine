import socket


TCP_IP = '18-220-130-220'
TCP_PORT = 8089
BUFFER_SIZE = 2048
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", data)
