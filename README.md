# CS7012 Management Of Networks & Distributed Systems (Group Project)

Managing MapReduce with SNMP.

Currently using Python 2.7 with PySNMP library & Mininet for managing virtual instances.
### Setup Mininet
http://www.brianlinkletter.com/set-up-mininet/

### Configure Mininet
1. ### In  Mininet vm
`$ sudo dhclient eth1`<br>
`$ ifconfig eth1`

2. ### In Terminal
`$ ssh -Y mininet@192.168.56.101` <br>
or <br>
`$ ssh -X mininet@192.168.56.101`

The IP address is the lower bound IP address when setting up the virtual box host.

## Start

Clone this Git repository in mininet VM and CD into it. <br>

## Install Dependencies in Mininet VM:

+ `$ chmod +rx install.sh` <br>
+ `$ ./install.sh` <br>


### Run the Setup

1. #### Start Mininet topology
`$ sudo ./bigdataSNMP.py`

2. #### Launch xterms of Hosts
`mininet> xterm h1 h2 h3 h4
`
2. #### Start SNMP Mapper 1 Agent on h1 xterm
`$ python agent.py` <br>
Runs a `UDP server` on port `1161` to accept incoming connections, has
`OIB that runs MapReduce`

3. #### Start SNMP Mapper 2 Agent on h2 xterm
`$ python agent.py` <br>

4. #### Start SNMP Reducer Agent on h3 xterm
`$ python agent.py` <br>

3. #### Start SNMP Manager on h4 xterm
`$ python manager.py` <br>

Note- Executes the OIB `SysDesr class` in agent which does word count. <br>
`manager.py` reads the file `test.txt`, and divides the file into two parts. <br>
It subsequently sends the files to h1 and h2. h1 and h2 will perform the map function and the shuffler <br>
function. Then h1 and h2 send the result in JSON format to h3. <br>
h3 works as a reducer and generates the final result, and saves it to `result.txt`.

### Mininet Python API

https://github.com/mininet/mininet/wiki/Introduction-to-Mininet

### Aditional Dependencies
[Twisted](http://pysnmp.sourceforge.net/examples/hlapi/twisted/contents.html) <br>


### Config SNMPd
Reference: http://www.it-slav.net/blogs/2009/02/05/install-and-configure-snmp-on-ubuntu/  

mv /etc/snmp/snmpd.conf  /etc/snmp/snmpd.conf.org  

Create a new /etc/snmp/snmpd.conf file:  
rocommunity  public  
syslocation  "TCD"
syscontact  test@test.ie  

Edit /etc/default/snmpd:   

Change from:
`# snmpd options (use syslog, close stdin/out/err).
SNMPDOPTS='-Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid 127.0.0.1'  `
To:
`# snmpd options (use syslog, close stdin/out/err).
 #SNMPDOPTS='-Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid 127.0.0.1'
 SNMPDOPTS='-Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid -c /etc/snmp/snmpd.conf'`



