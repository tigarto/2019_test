#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2 ):
	switch = self.addSwitch( 's1' )
	for h in range(n):
	    # Each host gets 50%/n of system CPU
	    host = self.addHost( 'h%s' % (h + 1),
		                 cpu=.5/n )
	    # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
	    self.addLink( host, switch, bw=10, delay='5ms', loss=2,
                          max_queue_size=1000, use_htb=True )


class SimpleNet( Mininet ):
    "Single switch connected to n hosts."
    def build( self ):
        topo = SingleSwitchTopo( n=4 )
        self.buildFromTopo( topo=topo,
	           host=CPULimitedHost, link=TCLink )
        self.start()
        print "Dumping host connections"
        dumpNodeConnections( self.hosts )
        print "Testing network connectivity"
        self.pingAll()
        print "Testing bandwidth between h1 and h4"
        h1, h4 = self.get( 'h1', 'h4' )
        self.iperf( (h1, h4) )
        self.stop()

        


tests = { 'perf_test': SimpleNet }
topos = { 'topo_test1': SingleSwitchTopo}

"""
invocacion desde la consola
sudo mn --custom test2.py --test perf_test

"""

