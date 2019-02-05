from mininet.net import Mininet
from mininet.log import info, setLogLevel
from time import time
from subprocess import Popen, PIPE
from select import poll, POLLIN
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
import timeit

"""
Proceso de test:

sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py

sudo python experimento.py


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
    hDst.cmd('kill %iperf')
    info('*** Stopping network')


def test1():
    info('*** Create the controller \n')

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

    iperfTest(h1, h2, outfile = 'iperf.out', errfile = 'iperf.err', seconds = 10, tprint = 0.5)

    info('*** Stopping network')
    net.stop()


def pingTest( hSrc, hDst, outfile = 'ping.out', errfile = 'ping.err', intervalo = 1, seconds=3 ):
    hSrc.cmd('echo >', outfile)
    hSrc.cmd('echo >', errfile)
    # Start pings
    hSrc.cmdPrint('ping', hDst.IP(),'-i',intervalo,
               '>', outfile,
               '2>', errfile,
               '&')
    info( "Monitoring output for", seconds, "seconds\n" )
    for h, line in monitorFiles( hSrc,outfile, seconds, timeoutms=intervalo ):
        if h:
            info( '%s: %s\n' % ( h.name, line ) )
    hSrc.cmd('kill %ping')

def test2():
    info('*** Create the controller \n')

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

    pingTest( h1, h2, outfile = 'ping.out', errfile = 'ping.err', intervalo = 0.5, seconds=10 )

    info('*** Stopping network')
    net.stop()

def test3():
    info('*** Create the controller \n')

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

    iperfTest2(h1, h2, h3, outfile='iperf_ataque.out', errfile='iperf_ataque.err', seconds=200, tprint=0.5)
    info('*** Stopping network')
    net.stop()

def lanzarAtaque(A, V):
    A.cmdPrint('hping3', '--flood', '--random-source', V.IP(),'&')

def iperfTest2(A, C, V, outfile = 'iperf_ataque.out', errfile = 'iperf_ataque.err', seconds=3, tprint = 0.5 ):
    C.cmd('echo >', outfile)
    C.cmd('echo >', errfile)
    # Start iperf server
    info("*** Starting iperf server... ***\n")
    V.cmdPrint('iperf', '-s', '&')  # El & es  necesario paara que no se bloque el programa
    info("*** Starting iperf client... ***\n")
    C.cmdPrint('iperf', '-c', str(V.IP()), '-i', str(tprint), '-t ' + str(seconds),
                  '>', outfile,
                  '2>', errfile, '&')
    lanzarAtaque(A,V)
    info("Monitoring output for", seconds, "seconds\n")
    for h, line in monitorFiles(C, outfile, seconds, timeoutms=500):
        if h:
            info('%s: %s\n' % (h.name, line))

    C.cmd('kill %iperf')
    V.cmd('kill %iperf')
    A.cmd('kill %hpin3')
    info('*** Stopping network')


if __name__ == '__main__':
    # test1() # Test de la funcion iperf sin ataque alguno
    # test2() # Test de la funcion ping
    print "Ejemplo lanzando un ataque"
    start_time = time()
    print start_time
    test3()
    end_time = time()
    print end_time
    elapsed_time = end_time - start_time
    print elapsed_time




