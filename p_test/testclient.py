#!/usr/bin/env python
# Information Example 

from socket import *

HOST = '172.17.0.2'
PORT = 9999
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

# while True:
#     # data = input('> ')
#     # if not data:
#     # 	break
data = "helo"
tcpCliSock.send(data)
data = tcpCliSock.recv(BUFSIZ)
if not data:
	pass
print(data.decode('utf-8'))
# tcpCliSock.close()
