#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

SNMP_START_CMD = '/etc/init.d/snmpd restart'
SNMP_WALK_CMD = 'snmpwalk -v 1 -c public -O e '
SNMP_WALK_OUT = "hopt.out"

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    info( '*** Add links\n')
    net.addLink(s1, h4)
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(s1, h3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()
    info( '*** Starting switches\n')
    net.get('s1').start([])

    info( '*** Post configure switches and hosts\n')
    hosts = [h1, h2, h3, h4]
    printInfo(hosts)
    h1.cmd(SNMP_START_CMD)
    CLI(net)
    net.stop()

def printInfo(hosts):
    for h in hosts:
        print "Host", h.name, "has IP address", h.IP()
    print "Run agent on host h1, master can be run anywhere"

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

