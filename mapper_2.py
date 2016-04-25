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
import re

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
        test = "it it it it ti ti ti ti"
        ans = self.word_count(test.strip().split(" "))
#    print(str(ans).strip('[]'))
        return api.protoModules[protoVer].OctetString(
            'Mapper 2, taking care of mapping and shuffling function'
            )
    def group_by_word(self, words):
        result = defaultdict(list)

        for (word, c) in words:
            result[word].append(c)

        return result


    def map_word(self, word):
        return word, 1


    def reduce_count(self, word, sequence):
        return word, sum(sequence)


    def word_count(self, document):
        self.mapper = Mapper(self.map_word, document)
        self.shuffler = Shuffler(self.group_by_word, self.mapper.run())
        self.reducer = Reducer(self.reduce_count, self.shuffler.run().iteritems())

        return self.reducer.run()




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
    udp.domainName, udp.UdpSocketTransport().openServerMode(('10.0.0.2', 1161))
)


## Local domain socket
#transportDispatcher.registerTransport(
#    unix.domainName, unix.UnixSocketTransport().openServerMode('/tmp/snmp-agent')
#)
IP = "10.0.0.2"
port = 1162

def listen_for_data():
    sock = socket.socket(socket.AF_INET,
					socket.SOCK_DGRAM)
    sock.bind((IP, port))
    while 1:
        data_recv = ""
        data, addr = sock.recvfrom(8192)
        try:
            while(data):
                data_recv = data_recv + data + "\n"
                sock.settimeout(2)
                data, addr = sock.recvfrom(8192)
        except socket.timeout:
            sock.close()
            sock = socket.socket(socket.AF_INET,
							socket.SOCK_DGRAM)
            sock.bind((IP, port))
            print "file transmition completed"
        mapper = Mapper(word_count.map_word, re.split(" |\\n|\\t|\\r",data_recv.strip()))
        shuffler = Shuffler(word_count.group_by_word, mapper.run())
        result = shuffler.run()
        print result
        result_json = json.dumps(result)
        print result_json
        reducer_port = 1162
        sock2 = socket.socket(socket.AF_INET,
						socket.SOCK_DGRAM)
        result_len = len(result_json)
        buf = 4096
        start = 0
        while (start + buf) < result_len:
            sock2.sendto(result_json[start:start+buf],(reducer, reducer_port))
            start = start + buf
        sock2.sendto(result_json[start:],(reducer, reducer_port))

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
#threading.Thread(target=listen_for_data, args=()).start()
#threading.Thread(target=listen_for_snmp, args=()).start()
except:
    raise
    print "Error to start thread"
while 1:
    pass
