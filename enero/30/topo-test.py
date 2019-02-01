#!/usr/bin/python

"""
This example shows how to create a network and run multiple tests.
For a more complicated test example, see udpbwtest.py.
"""

from mininet.cli import CLI
from mininet.node import OVSKernelSwitch
from mininet.topolib import TreeTopo
from mininet.util import custom, pmonitor
from mininet.log import setLogLevel, info
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.link import TCLink

import time
import os
setLogLevel( 'info' )


# sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py


def getPing( h1, h2, veces ):
    popens = {}
    popens[h1] = h1.popen("ping -c %s %s" %(veces, h2.IP()))
    # Monitor them and print output
    #host, line = pmonitor(popens)
    #info("<%s>: %s" % (host.name, line))
    for host, line in pmonitor(popens):
        if host:
            info("<%s>: %s" % (host.name, line))
    # Done


setLogLevel('info')

info('*** Create the controller \n')

#info(c0)
"Create Simple topology example."
net = Mininet(switch = OVSSwitch, build=False, link=TCLink)
net.addController('c0', controller = RemoteController, ip = "127.0.0.1", port = 6653)
# Initialize topology

# Add containers
h1 = net.addHost('h1', ip='10.0.0.251')  # Cliente
h2 = net.addHost('h2', ip='10.0.0.252')  # Atacante
h3 = net.addHost('h3', ip='10.0.0.253')  # Victima

# Add switches
info('*** Adding switches\n')
sw1 = net.addSwitch('sw1', protocols='OpenFlow13')

# Add links
info('*** Creating links\n')
net.addLink( h1, sw1, bw = 1000 )
net.addLink( h2, sw1, bw = 1000 )
net.addLink( h3, sw1, bw = 1000 )

# Build the network
info('*** Build the network\n')
net.build()

info('*** Starting network\n')
net.start()

getPing( h1, h2, 5)
#info('*** Running CLI\n')
#CLI(net)

info('*** Stopping network')
net.stop()


