from mininet.node import Controller
from os import environ
from mininet.log import setLogLevel,info,debug

POXDIR = environ[ 'HOME' ] + '/pox-1.3'

setLogLevel( 'debug' )

class POX( Controller ):
    def __init__( self, name, cdir=POXDIR,
                  command= POXDIR + ' python pox.py',
                  cargs=( 'openflow.of_04 --port=%s '
                          'forwarding.l2_learning_04' ),
                  **kwargs ):
        Controller.__init__( self, name, cdir=cdir,
                             command=command,
                             cargs=cargs, 
                             **kwargs )

"""
def start( self ):
        

        pathCheck( self.command )
        cout = '/tmp/' + self.name + '.log'
        if self.cdir is not None:
            self.cmd( 'cd ' + self.cdir )
        self.cmd( self.command + ' ' + self.cargs % self.port +
                  ' 1>' + cout + ' 2>' + cout + ' &' )
        self.execed = False


class Controller( Node ):

    def __init__( self, name, inNamespace=False, command='controller',
                  cargs='-v ptcp:%d', cdir=None, ip="127.0.0.1",
                  port=6653, protocol='tcp', **params ):
        self.command = command
        self.cargs = cargs
        self.cdir = cdir
        # Accept 'ip:port' syntax as shorthand
        if ':' in ip:
            ip, port = ip.split( ':' )
            port = int( port )
        self.ip = ip
        self.port = port
        self.protocol = protocol
        Node.__init__( self, name, inNamespace=inNamespace,
                       ip=ip, **params  )
        self.checkListening()


class POX( Controller ):
    def __init__( self, name, cdir=POXDIR,
                  command='python pox.py',
                  cargs=( 'openflow.of_01 --port=%s '
                          'forwarding.l2_learning' ),
                  **kwargs ):
        Controller.__init__( self, name, cdir=cdir,
                             command=command,
                             cargs=cargs, **kwargs )



self.command +  self.cargs % self.port ' 1>' + cout + ' 2>' + cout + ' &'

cargs=( 'openflow.of_01 --port=%s ''forwarding.l2_learning' )
python pox.py


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

"""



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

