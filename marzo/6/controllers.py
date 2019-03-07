from mininet.node import Controller
from os import environ

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



class RYU( Controller ):
    def __init__(self, name, ryuArgs = 'simple_switch_13.py', **kwargs):
        if ryuArgs == None:
            ryuArgs = 'simple_switch_13.py'        
        Controller.__init__(self, name,
                            command = '/usr/local/bin/ryu-manager',
                            cargs='--ofp-tcp-listen-port %s ' + ryuArgs,
                            **kwargs)

controllers={ 'pox': POX,
              'ryu': RYU }
