import socket
import sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#ost = '111.230.243.128'
#port = 4148

host = input("请输入IP地址")
port = int(input("端口"))
s.connect((host,port))
while True:
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    print(msg)
    if msg.find('<input>') > -1:
        
        send = input("请输入\r\n")
        if send == "":
            send = "没有输入指令"
        s.send(send.encode('utf-8'))

    if msg.find('疮了') > -1:
        input("输入任意结束")
        s.close()
        break