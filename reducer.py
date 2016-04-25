#Listen and respond to SNMP GET/GETNEXT queries
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp, udp6, unix
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api
import time, bisect
from src.map_reduce import Mapper, Reducer, Shuffler
from collections import defaultdict
import word_count
import thread
import socket
import json


mapper_1 = "10.0.0.1"
mapper_2 = "10.0.0.2"
reducer = "10.0.0.3"
manager = "10.0.0.4"

class SysDescr:
    name = (1,3,6,1,2,1,1,1,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        return api.protoModules[protoVer].OctetString(
            'Reducer, taking care of the reduce function'
            )

class Uptime:
    name = (1,3,6,1,2,1,1,3,0)
    birthday = time.time()
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        return api.protoModules[protoVer].TimeTicks(
            (time.time()-self.birthday)*100
            )

mibInstr = (
    SysDescr(), Uptime(),  # sorted by object name
    )

mibInstrIdx = {}
for mibVar in mibInstr:
    mibInstrIdx[mibVar.name] = mibVar

def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    while wholeMsg:
        msgVer = api.decodeMessageVersion(wholeMsg)
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
            )
        rspMsg = pMod.apiMessage.getResponse(reqMsg)
        rspPDU = pMod.apiMessage.getPDU(rspMsg)
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        varBinds = []; pendingErrors = []
        errorIndex = 0
        # GETNEXT PDU
        if reqPDU.isSameTypeWith(pMod.GetNextRequestPDU()):
            # Produce response var-binds
            for oid, val in pMod.apiPDU.getVarBinds(reqPDU):
                errorIndex = errorIndex + 1
                # Search next OID to report
                nextIdx = bisect.bisect(mibInstr, oid)
                if nextIdx == len(mibInstr):
                    # Out of MIB
                    varBinds.append((oid, val))
                    pendingErrors.append(
                        (pMod.apiPDU.setEndOfMibError, errorIndex)
                        )
                else:
                    # Report value if OID is found
                    varBinds.append(
                        (mibInstr[nextIdx].name, mibInstr[nextIdx](msgVer))
                        )
        elif reqPDU.isSameTypeWith(pMod.GetRequestPDU()):
            for oid, val in pMod.apiPDU.getVarBinds(reqPDU):
                if oid in mibInstrIdx:
                    varBinds.append((oid, mibInstrIdx[oid](msgVer)))
                else:
                    # No such instance
                    varBinds.append((oid, val))
                    pendingErrors.append(
                        (pMod.apiPDU.setNoSuchInstanceError, errorIndex)
                        )
                    break
        else:
            # Report unsupported request type
            pMod.apiPDU.setErrorStatus(rspPDU, 'genErr')
        pMod.apiPDU.setVarBinds(rspPDU, varBinds)
        # Commit possible error indices to response PDU
        for f, i in pendingErrors:
            f(rspPDU, i)
        transportDispatcher.sendMessage(
            encoder.encode(rspMsg), transportDomain, transportAddress
            )
    return wholeMsg

transportDispatcher = AsyncoreDispatcher()
transportDispatcher.registerRecvCbFun(cbFun)

# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(('10.0.0.3', 1161))
)


## Local domain socket
#transportDispatcher.registerTransport(
#    unix.domainName, unix.UnixSocketTransport().openServerMode('/tmp/snmp-agent')
#)
IP = "10.0.0.3"
port = 1162

def listen_for_data():
    sock = socket.socket(socket.AF_INET,
					socket.SOCK_DGRAM)
    sock.bind((IP, port))
    while 1:
        data1_recv = ""
        data2_recv = ""
        data, addr = sock.recvfrom(8192)
        addr1 = addr
        try:
            while(data):
                if addr == addr1:
                    data1_recv = data1_recv + data
                    print "get data from 1"
                else:
                    data2_recv = data2_recv + data
                    print "get data from 2"
                sock.settimeout(3)
                data, addr = sock.recvfrom(8192)
        except socket.timeout:
            sock.close()
            sock = socket.socket(socket.AF_INET,
							socket.SOCK_DGRAM)
            sock.bind((IP, port))
            print "reducer got everything" 
        data1_dict = json.loads(data1_recv)
        data2_dict = json.loads(data2_recv)
        data_result = data1_dict.copy()
        for key in data2_dict.keys():
            if key in data_result:
                data_result[key] = data_result[key] + data2_dict[key]
            else:
                data_result[key] = data2_dict[key]
        reducer = Reducer(word_count.reduce_count, data_result.iteritems())
        result = reducer.run()
        print result
        file_out = open("result.txt","w")
        for word in result:
            file_out.write(str(word) + "\n")
        file_out.close()

def listen_for_snmp():
    transportDispatcher.jobStarted(1)

    try:
    # Dispatcher will never finish as job#1 never reaches zero
        transportDispatcher.runDispatcher()
    except:
        transportDispatcher.closeDispatcher()
        raise


try:
	thread.start_new_thread(listen_for_data,())
	thread.start_new_thread(listen_for_snmp,())
except:
    raise
    print "Error to start thread"
while 1:
    pass
