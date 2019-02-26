from mininet.node import Controller
from os import environ

class RYU( Controller ):
    def __init__( self, name, params=('simple_switch_13.py','ofctl_rest.py'),
                  **kwargs ):
        Controller.__init__( self, name, params = params, **kwargs )

controllers={ 'ryu': RYU }


