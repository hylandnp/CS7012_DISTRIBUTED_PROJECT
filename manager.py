from twisted.internet.task import react
from pysnmp.hlapi.twisted import *
import socket
import threading


mapper_1 = "10.0.0.1"
mapper_2 = "10.0.0.2"
reducer = "10.0.0.3"
manager = "10.0.0.4"

def file_processing():
    file_in = open("test.txt","r")
    num_lines = sum(1 for line in file_in)
    file_in.close()
    file_in = open("test.txt","r")
    file1 = ""
    file2 = ""
    count = 0
    for line in file_in:
	if count < num_lines/2:
		file1+=(line + "\n")
		count = count + 1
	else:
		file2+=(line + "\n")
		count += 1
    file_in.close()
    return file1, file2

def send_file(file1, file2):
    port = 1162
    sock = socket.socket(socket.AF_INET,
					socket.SOCK_DGRAM)
    len1 = len(file1)
    len2 = len(file2)
    buf = 4096
    start = 0
    while ((start + buf) < len1):
        sock.sendto(file1[start:start+buf],(mapper_1, port))
        start = start + buf
    sock.sendto(file1[start:],(mapper_1, port))
    start = 0
    while ((start + buf) < len2):
        sock.sendto(file2[start:start+buf],(mapper_2, port))
        start = start + buf
    sock.sendto(file2[start:],(mapper_2, port))
    sock.close()	
    

file1, file2 = file_processing()
send_file(file1, file2)
