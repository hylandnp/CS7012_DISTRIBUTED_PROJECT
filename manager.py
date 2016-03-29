from twisted.internet.task import react
from pysnmp.hlapi.twisted import *
import socket

mapper_1 = "10.0.0.1"
mapper_2 = "10.0.0.2"
reducer = "10.0.0.3"
manager = "10.0.0.4"

def file_processing():
    file_in = open("test.txt","r")
    num_lines = sum(1 for line in file_in)
    file_in.close()
    file_in = open("test.txt","r")
    print num_lines
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
    sock.sendto(file1, (mapper_1, port))
    sock.sendto(file2, (mapper_2, port))	
    
    

def success((errorStatus, errorIndex, varBinds), hostname):
    if errorStatus:
        print('%s: %s at %s' % (
                hostname,
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1][0] or '?'
            )
        )
    else:
        for varBind in varBinds:
            print(' = '.join([ x.prettyPrint() for x in varBind ]))

def failure(errorIndication, hostname):
    print('%s failure: %s' % (hostname, errorIndication))

def getSysDescr(reactor, hostname):
    d = getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget(('10.0.0.1', 1161)),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')))
#ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')))

    d.addCallback(success, hostname).addErrback(failure, hostname)

    return d

file1, file2 = file_processing()
send_file(file1, file2)
react(getSysDescr, ['10.0.0.1'])
