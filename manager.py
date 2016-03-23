from twisted.internet.task import react
from pysnmp.hlapi.twisted import *

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
               UdpTransportTarget(('localhost', 1161)),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')))

    d.addCallback(success, hostname).addErrback(failure, hostname)

    return d

react(getSysDescr, ['localhost'])
