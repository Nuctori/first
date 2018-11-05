import socket
import sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '127.0.0.1'
port = 4148
s.connect((host,port))
while True:
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    print(msg)
    if msg.find('<input>') > -1:
        send = input("请输入\r\n")
        s.send(send.encode('utf-8'))

s.close()
