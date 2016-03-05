from pysnmp.hlapi import *

g = setCmd(SnmpEngine(),
	CommunityData('public'),
	UdpTransportTarget(('localhost', 161)),
	ContextData(),
	ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

print next(g)