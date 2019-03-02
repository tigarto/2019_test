import os
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from mininet.topo import Topo
import subprocess
from time import time, sleep
import psutil
from mininet.cli import CLI
from subprocess import Popen, PIPE, STDOUT
from select import poll, POLLIN
##
from controlador import RYU, POX

class UnidadExperimental:
    def __init__(self, topo = None, controller = None):
        self.topo = topo
        self.controller = controller
        self.atacante = None
        self.victima = None
        self.cliente = None

    def setTopo(self,topo):
        self.topo = topo

    # Puede que sea necesario revisarlo
    def setController(self,controller,appsController = 'simple_switch_13.py'):
        if controller == 'ryu':
            self.controller = RYU(name='c0',
                                  ryuArgs =appsController)
        else:
            self.controller = POX() # Mejorar
    def getTopo(self):
        return self.topo

    def getController(self):
        return self.controller

    def definirNodosClaves(self,A = None,C = None ,V = None):
        self.atacante = A
        self.cliente = C
        self.victima = V

    def obtenerNodosClaves(self):
        return [self.atacante, self.cliente, self.victima]
