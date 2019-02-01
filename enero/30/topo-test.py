#!/usr/bin/python

"""
Simple example of sending output to multiple files and
monitoring them
"""


from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from time import time
from select import poll, POLLIN
from subprocess import Popen, PIPE
from mininet.link import TCLink

'''
https://www.incapsula.com/cdn-guide/glossary/round-trip-time-rtt.html
http://www.ateam-oracle.com/testing-latency-and-throughput/
'''

# sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
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


def pingTest( hSrc, hDst, seconds=3 ):
    outfile = 'ping.out'
    errfile = 'ping.err'
    hSrc.cmd('echo >', outfile)
    hSrc.cmd('echo >', errfile)
    # Start pings

    hSrc.cmdPrint('ping', hDst.IP(),
               '>', outfile,
               '2>', errfile,
               '&')
    info( "Monitoring output for", seconds, "seconds\n" )
    for h, line in monitorFiles( hSrc,outfile, seconds, timeoutms=500 ):
        if h:
            info( '%s: %s\n' % ( h.name, line ) )
    hSrc.cmd('kill %ping')


def iperfTest( hSrc, hDst, seconds=3 ):
    outfile = 'iperf.out'
    errfile = 'iperf.err'
    hSrc.cmd('echo >', outfile)
    hSrc.cmd('echo >', errfile)
    # Start pings
    '''
    hDst.cmdPrint('iperf', '-s', '-i', '0.5', '&')
    
    hSrc.cmdPrint('iperf', '-c', str(hDst.IP()), '-t ' + str(seconds),
                  '>', outfile,
                  '2>', errfile,
                  '&')
    '''
    hDst.cmdPrint('iperf', '-s', '&')
    hSrc.cmdPrint('iperf', '-c', str(hDst.IP()), '-i' , str(seconds/4.0),'-t ' + str(seconds),
                  '>', outfile,
                  '2>', errfile,
                  '&')
    info( "Monitoring output for", seconds, "seconds\n" )
    sleep(seconds + 2)
    '''
    for h, line in monitorFiles( hSrc, outfile, seconds, timeoutms=500 ):
        if h:
            info( '%s: %s\n' % ( h.name, line ) )
    '''
    hSrc.cmd('kill %iperf')
    hSrc.cmd('kill %iperf')

'''
def pingTest2(hSrc, hDst, seconds):
    outfile = 'ping2.out'
    errfile = 'ping2.err'
    hSrc.cmd('echo >', outfile)
    hSrc.cmd('echo >', errfile)
    hSrc.cmd('echo >', outfile)
    hSrc.cmd('echo >', errfile)
    hSrc.cmdPrint('ping', hDst.IP(),
                  '>', outfile,
                  '2>', errfile,
                  '&')
    info("Monitoring output for", seconds, "seconds\n")
    sleep(seconds)
    hSrc.cmd('kill %ping')
'''

info('*** Create the controller \n')

#info(c0)
"Create Simple topology example."
net = Mininet(switch = OVSSwitch, build=False, link=TCLink)
net.addController('c0', controller = RemoteController, ip = "127.0.0.1", port = 6653)
# Initialize topology

# Add containers
h1 = net.addHost('h1', ip='10.0.0.251')  # Cliente
h2 = net.addHost('h2', ip='10.0.0.252')  # Atacante
h3 = net.addHost('h3', ip='10.0.0.253')  # Victima

# Add switches
info('*** Adding switches\n')
sw1 = net.addSwitch('sw1', protocols='OpenFlow13')

# Add links
info('*** Creating links\n')
net.addLink( h1, sw1, bw = 1000 )
net.addLink( h2, sw1, bw = 1000 )
net.addLink( h3, sw1, bw = 1000 )

# Build the network
info('*** Build the network\n')
net.build()

info('*** Starting network\n')
net.start()

#pingTest(h1, h2, 5)
pingTest(h1, h2, 5)
iperfTest(h1,h2,10)
#info('*** Running CLI\n')
#CLI(net)

info('*** Stopping network')
net.stop()
