#!/usr/bin/python

from mininet.log import setLogLevel
from mininet.net import Mininet,Controller
from mininet.topolib import TreeTopo
from mininet.cli import CLI
from os import environ

# We assume you are in the same directory as pox.py
# or that it is loadable via PYTHONPATH

setLogLevel( 'info' )

POXDIR = environ[ 'HOME' ] + '/pox'

class POX( Controller ):
    def __init__( self, name, cdir=POXDIR,
                  command='python pox.py',
                  cargs=( 'openflow.of_01 --port=%s '
                          'forwarding.l2_learning' ),
                  **kwargs ):
        Controller.__init__( self, name, cdir=cdir,
                             command=command,
                             cargs=cargs, **kwargs )



net = Mininet( topo=TreeTopo( depth=2, fanout=2 ),
               controller=POX('c0') )

net.start()
CLI( net )
net.stop()