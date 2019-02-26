#!/usr/bin/python

from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.cli import CLI

# We assume you are in the same directory as pox.py
# or that it is loadable via PYTHONPATH
from ryu import RYU

setLogLevel( 'info' )

net = Mininet( topo=TreeTopo( depth=2, fanout=2 ),
               controller=RYU )

net.start()
CLI( net )
net.stop()
