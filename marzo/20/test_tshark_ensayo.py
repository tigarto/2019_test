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
from time import sleep




if __name__ == "__main__":
    
    comando = "sudo tshark -i lo -d tcp.port==6653,openflow -O openflow_v4 -F pcap -w ca_of1.pcap"
    pid_hijo = os.popen(comando)   
    sleep(10)
    pid_hijo.SIGKILL


# hping3 --flood --rand-source 10.0.0.3
