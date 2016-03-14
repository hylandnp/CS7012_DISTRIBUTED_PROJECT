# CS7012 Management Of Networks & Distributed Systems (Group Project)

Managing MapReduce with SNMP.

Currently using Python 2.7 with PySNMP library & Mininet for managing virtual instances.

## Setup Mininet
http://www.brianlinkletter.com/set-up-mininet/

## Configure Mininet
### In  Mininet vm
$ sudo dhclient eth1
$ ifconfig eth1

### In Terminal
`$ ssh -Y mininet@192.168.56.101` <br>
or <br> 
`$ ssh -X mininet@192.168.56.101`

The IP address is the lower bound IP address when setting up the virtual box host.

password: mininet

## Setup Notes

http://www.it-slav.net/blogs/2009/02/05/install-and-configure-snmp-on-ubuntu/ and https://kspviswa.wordpress.com/2015/06/20/how-to-run-snmp-agents-clients-inside-mininet-hosts/ to setup SNMPd with Mininet on the Mininet VM (see second link for VM downloads).

##Install Dependencies in Mininet VM:

`$ chmod +rx install.sh` <br>
`$ ./install.sh` <br>


##Start

Clone this Git repository into a folder and CD into it. <br> 
'$ chmod 777 snmpTest.py'
Run `$ sudo ./snmpTest.py` to check if SNMP runs in the Mininet VM.

##Mininet Python API

https://github.com/mininet/mininet/wiki/Introduction-to-Mininet

##Config SNMPd
Reference: http://www.it-slav.net/blogs/2009/02/05/install-and-configure-snmp-on-ubuntu/  
  
mv /etc/snmp/snmpd.conf  /etc/snmp/snmpd.conf.org  
  
Create a new /etc/snmp/snmpd.conf file:  
rocommunity  public  
syslocation  "TCD"
syscontact  test@test.ie  
  
Edit /etc/default/snmpd:   

Change from:
># snmpd options (use syslog, close stdin/out/err).
>SNMPDOPTS='-Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid 127.0.0.1'  
To:
># snmpd options (use syslog, close stdin/out/err).
>#SNMPDOPTS='-Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid 127.0.0.1'
>SNMPDOPTS='-Lsd -Lf /dev/null -u snmp -I -smux -p /var/run/snmpd.pid -c /etc/snmp/snmpd.conf'

