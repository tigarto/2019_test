#!/usr/bin/python

from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.cli import CLI

# We assume you are in the same directory as pox.py
# or that it is loadable via PYTHONPATH
from controllers import RYU,POX
import os



setLogLevel( 'info' )



# ENSAYO CON POX --> ok
net = Mininet( topo=TreeTopo( depth=2, fanout=2 ),
               controller=POX )

if __name__ == "__main__":
  net.start()
  net.pingAll() 
  net.iperf()
  net.stop()

