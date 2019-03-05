import os
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from mininet.topo import Topo
import subprocess
from time import time, sleep
import psutil
from mininet.cli import CLI
from subprocess import Popen, PIPE, STDOUT
from select import poll, POLLIN
from os import environ

class RYU( Controller ):
    def __init__(self, name, ryuArgs = 'simple_switch_13.py', **kwargs):
        Controller.__init__(self, name,
                            command = '/usr/local/bin/ryu-manager',
                            cargs='--ofp-tcp-listen-port %s ' + ryuArgs,
                            **kwargs)

POXDIR = environ[ 'HOME' ] + '/pox-1.3'

class POX( Controller ):
    def __init__( self, name, cdir=POXDIR,
                  command='python pox.py',
                  poxArgs = 'forwarding.l2_learning_04',
                  **kwargs ):
        if poxArgs == None:
            poxArgs = 'forwarding.l2_learning_04'
        cargs = 'openflow.of_04 --port=%s ' + poxArgs
        Controller.__init__( self, name, cdir=cdir,
                             command=command,
                             cargs=cargs, **kwargs )

