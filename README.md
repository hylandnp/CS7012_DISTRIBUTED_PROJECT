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

`$ sudo apt-get install python-pip` <br>
`$ sudo apt-get install python-virtualenv` <br>
`$ sudo apt-get install python-dev` <br>
`$ virtualenv env` <br>
`$ source env/bin/activate` <br>
`$ sudo apt-get install snmpd` <br>
`$ sudo pip install pysnmp` <br>
`$ pip install -r requirements.txt` <br>


##Start

Clone this Git repository into a folder and CD into it. <br> 
Run `$ sudo python ./snmpTest.py` to check if SNMP runs in the Mininet VM.

##Mininet Python API

https://github.com/mininet/mininet/wiki/Introduction-to-Mininet