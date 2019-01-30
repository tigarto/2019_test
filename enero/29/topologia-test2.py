#!/usr/bin/python

'''
Topologia:

        c0  c1
         \  /
          \/
   h1 --- s1 --- h3
          |
          |
          h2

Donde c0 y c1 son controladores externos

sudo python topologia-test2.py 

Controlador: 

./pox.py log.level --DEBUG openflow.of_01 --port=6653 forwarding.l2_learning 


Comandos de apoyo (por si acaso):
1. sudo netstat -tlp
2. sudo fuser -k tcp 6653 (https://gist.github.com/happyrobots/1101053)
3. sudo ovs-vsctl show

Enlaces:
https://blog.axosoft.com/gitkraken-tips-2/
'''

from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.net import Containernet
from mininet.log import info, setLogLevel
from mininet.link import TCLink

import time

import os

setLogLevel('info')

info('*** Create the controller \n')

#info(c0)
"Create Simple topology example."
net = Containernet(switch = OVSSwitch, build=False, link=TCLink)
net.addController('c0', controller = RemoteController, ip = "127.0.0.1", port = 6653)
net.addController('c1', controller = RemoteController, ip = "127.0.0.1", port = 6654)
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
net.addLink( h1, sw1, bw = 10 )
net.addLink( h2, sw1, bw = 10 )
net.addLink( h3, sw1, bw = 10 )

# Build the network
info('*** Build the network\n')
net.build()

info('*** Starting network\n')
net.start()

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()
