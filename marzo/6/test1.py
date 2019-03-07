#!/usr/bin/python

from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.cli import CLI

# We assume you are in the same directory as pox.py
# or that it is loadable via PYTHONPATH
from controllers import RYU,POX
import os
import signal


setLogLevel( 'info' )


# ENSAYO CON RYU --> ok

net = Mininet( topo=TreeTopo( depth=2, fanout=2 ),
               controller=RYU('c0') )
"""


# ENSAYO CON POX --> ok
c0 = POX('c0') 
net = Mininet( topo=TreeTopo( depth=2, fanout=2 ),
               controller=c0)
"""


net_sw = {}
for k,v in net.items():
    if 's' in k:
        sw_int = []
        for i in range(1,len(v.ports)):
            sw_int.append(k + '-eth' + str(i))
        net_sw[k]=sw_int
        sw_int = []


filename="monitoreo.csv"
list_interfaces = ''
for k in net_sw:
    for int_sw in net_sw[k]:
        list_interfaces+=int_sw+','
list_interfaces = list_interfaces.rstrip(',')
        

comando = "bwm-ng -I " + \
            list_interfaces + \
            " -o csv -t 1000 -F " + \
            filename
print comando
pid_child = os.fork()
if pid_child == 0:
    # Proceso hijo
    os.system(comando)


else:
    net.start()
    #CLI( net )
    net.pingAll()
    net.iperf()
    net.stop()
    # No se espera el proceso de medicion en las interfaces pero se killea
    os.kill(pid_child,signal.SIGKILL)


