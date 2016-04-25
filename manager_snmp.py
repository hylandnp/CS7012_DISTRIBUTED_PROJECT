from twisted.internet.task import react
from pysnmp.hlapi.twisted import *
import socket
import threading
import sys

Ips = dict()
Ips["mapper_1"] = "10.0.0.1"
Ips["mapper_2"] = "10.0.0.2"
Ips["reducer"] = "10.0.0.3"
Ips["manager"] = "10.0.0.4"
mapper_1 = "10.0.0.1"
mapper_2 = "10.0.0.2"
reducer = "10.0.0.3"
manager = "10.0.0.4"

Objs = dict()
Objs['uptime'] = "1.3.6.1.2.1.1.3.0"
Objs['sysDescr'] = "1.3.6.1.2.1.1.1.0"

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

def getSysDescr(reactor, hostname, obj):
    d = getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget((hostname, 1161)),
               ContextData(),
# ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')))
#ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')))
               ObjectType(ObjectIdentity(obj)))
    d.addCallback(success, hostname).addErrback(failure, hostname)

    return d

target = Ips[sys.argv[1]]
target_obj = Objs[sys.argv[2]]
print "target: " + sys.argv[1] + ", object: " + sys.argv[2] 
react(getSysDescr, [target, target_obj])

