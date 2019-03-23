#!/usr/bin/python

from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.cli import CLI
from mininet.topo import SingleSwitchTopo
from signal import SIGKILL
# We assume you are in the same directory as pox.py
# or that it is loadable via PYTHONPATH
from controlador import RYU,POX
import os
import subprocess

if __name__ == "__main__":
    setLogLevel( 'info' )
    # Creando la red: RYU + Single topo
    net = Mininet( topo=SingleSwitchTopo(k = 3), controller=RYU('c0'))
    # Obteniendo las interfaces de los switches  
    """
    Lanzando el proceso asociado al comando
    """
    
    pid_hijo = os.fork()

    if pid_hijo == 0:
        # Proceso hijo 
        
        
        comando = "tshark -i lo -d tcp.port==6653,openflow -O openflow_v4 -F pcap > capture_of1.pcap &"
        info("%s\n"%(comando))
        os.system(comando)

    else:
        # Proceso padre
        info("Iniciando topologia mininet")
        net.start()
        CLI( net )
        net.stop()
        os.kill(pid_hijo.pid,SIGKILL)
    """
        info("Iniciando topologia mininet")
        net.start()
        CLI( net )
        net.stop()
        os.kill(pid_hijo,SIGKILL)
    """

# hping3 --flood --rand-source 10.0.0.3
