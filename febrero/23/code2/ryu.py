from mininet.node import Controller
from os import environ

class RYU( Controller ):
    def __init__(self, ryuArgs = 'simple_switch_13.py', name = 'c0', **kwargs):
        Controller.__init__(self, name = name,
                            command = '/usr/local/bin/ryu-manager',
                            cargs='--ofp-tcp-listen-port %s ' + ryuArgs,
                            **kwargs)

controllers={ 'ryu': RYU }


