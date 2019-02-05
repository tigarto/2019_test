from mininet.net import Mininet
from mininet.log import info, setLogLevel
from time import time
from subprocess import Popen, PIPE
from select import poll, POLLIN
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from mininet.topo import Topo

"""
Proceso de test:

sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py

sudo mn --custom experimento.py --topo topo1 --test test_iperf --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1:6653  --link=tc,bw=100 



"""


setLogLevel('info')

def monitorFiles(hSrc, outfile, seconds, timeoutms ):
    "Monitor set of files and return [(host, line)...]"
    devnull = open( '/dev/null', 'w' )
    tails, fdToFile, fdToHost = {}, {}, {}
    tail = Popen( [ 'tail', '-f', outfile ],
                      stdout=PIPE, stderr=devnull )
    fd = tail.stdout.fileno()
    fdToFile = tail.stdout
    fdToHost = hSrc
    # Prepare to poll output files
    readable = poll()
    readable.register( tail.stdout.fileno(), POLLIN )
    # Run until a set number of seconds have elapsed
    endTime = time() + seconds
    while time() < endTime:
        fdlist = readable.poll(timeoutms)
        if fdlist:
            for fd, _flags in fdlist:
                f = fdToFile
                # Wait for a line of output
                line = f.readline().strip()
                # yield host , decode( line )
                yield hSrc, line
        else:
            # If we timed out, return nothing
            yield None, ''
    for t in tails.values():
        t.terminate()
    devnull.close()  # Not really necessary


def iperfTest(hSrc, hDst, outfile = 'iperf.out', errfile = 'iperf.err', seconds=3, tprint = 0.5 ):
    hSrc.cmd('echo >', outfile)
    hSrc.cmd('echo >', errfile)
    # Start iperf server
    info("*** Starting iperf server... ***\n")
    hDst.cmdPrint('iperf', '-s', '&')  # El & es  necesario paara que no se bloque el programa

    info("*** Starting iperf client... ***\n")
    hSrc.cmdPrint('iperf', '-c', str(hDst.IP()), '-i', str(tprint), '-t ' + str(seconds),
                  '>', outfile,
                  '2>', errfile, '&')
    info("Monitoring output for", seconds, "seconds\n")
    for h, line in monitorFiles(hSrc, outfile, seconds, timeoutms=500):
        if h:
            info('%s: %s\n' % (h.name, line))

    hSrc.cmd('kill %iperf')
    hSrc.cmd('kill %iperf')
    info('*** Stopping network')
    net.stop()


class TopoTest1( Topo ):
    "Single switch connected to n hosts."
    def build(self):

        h1 = self.addHost('h1', ip='10.0.0.1')  # Cliente
        h2 = self.addHost('h2', ip='10.0.0.2')  # Atacante
        h3 = self.addHost('h3', ip='10.0.0.3')  # Victima

        # Add switches
        info('*** Adding switches\n')
        s1 = self.addSwitch('sw1', protocols='OpenFlow13')

        # Add links
        info('*** Creating links\n')
        self.addLink(h1, s1, bw=100)
        self.addLink(h2, s1, bw=100)
        self.addLink(h3, s1, bw=100)






def perfTest():
    "Create network and run simple performance test"
    topo = TopoTest1()
    net = Mininet( topo=topo , link=TCLink )
    net.start()
    print "Testing network connectivity"
    net.pingAll()
    h1, h2 = net.get('h1', 'h2')
    print "Testing bandwidth between h1 and h4"
    iperfTest(h1, h2, seconds = 10, tprint = 0.5)
    info('*** Stopping network')
    net.stop()


topos = { 'topo1': TopoTest1 }
tests = { 'test_perf': perfTest }

"""
sudo mn --topo=topo1 --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1:6653  

"""


"""
class MyTopo( Topo ):
   def build( self, ...):
def myTest( net ):
...
topos = { 'mytopo': MyTopo }
tests = { 'mytest': myTest }
"""

"""
if __name__ == '__main__':
    info('*** Create the controller \n')

    # info(c0)
    "Create Simple topology example."
    net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
    # Initialize topology

    # Add containers
    h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
    h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
    h3 = net.addHost('h3', ip='10.0.0.3')  # Victima

    # Add switches
    info('*** Adding switches\n')
    sw1 = net.addSwitch('sw1', protocols='OpenFlow13')

    # Add links
    info('*** Creating links\n')
    net.addLink(h1, sw1, bw=100)
    net.addLink(h2, sw1, bw=100)
    net.addLink(h3, sw1, bw=100)

    # Build the network
    info('*** Build the network\n')
    net.build()

    info('*** Starting network\n')
    net.start()

    # pingTest(h1, h2, 5)
    # pingTest(h1, h2, 100)
    iperfTest(h1, h2, seconds = 10, tprint = 0.5)
    # info('*** Running CLI\n')
    # CLI(net)

"""



