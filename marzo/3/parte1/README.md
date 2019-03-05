https://www.python-course.eu/forking.php
https://www.python-course.eu/os_module_shell.php
https://www.python-course.eu/pipes.php
https://www.python-course.eu/forking.php
https://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
https://noxrepo.github.io/pox-doc/html/

```
def start( self ):
        """Start <controller> <args> on controller.
           Log to /tmp/cN.log"""
        pathCheck( self.command )
        cout = '/tmp/' + self.name + '.log'
        if self.cdir is not None:
            self.cmd( 'cd ' + self.cdir )
        self.cmd( self.command + ' ' + self.cargs % self.port +
                  ' 1>' + cout + ' 2>' + cout + ' &' )
        self.execed = False


class Controller( Node ):
    """A Controller is a Node that is running (or has execed?) an
       OpenFlow controller."""

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

```

Para el readme toca sacar este machetazo:
http://sdnhub.org/tutorials/pox/

https://repository.javeriana.edu.co/bitstream/handle/10554/16498/ContrerasPardoCarlosAlberto2014.pdf?sequence=1


sudo mn --topo single,3 --mac --controller remote --switch ovsk

sudo ovs-vsctl set bridge s1 protocols=OpenFlow13





 sudo ./pox.py log.level --DEBUG forwarding.l2_learning_04
