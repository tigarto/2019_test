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
# 
from trafico import Trafico, TraficoAtaque, TraficoNormal
from unidad_experimental import UnidadExperimental

class Experimento:
    def __init__(self):
        self.net = None
        self.inputs = None
        self.trafico = None

    def configureParams(self,ue):
        self.inputs = ue
        self.net = Mininet( controller=ue.getController(),
                            switch=OVSSwitch,
                            build=False,
                            link=TCLink,
                            topo = ue.getTopo()
                          )
        self.net.build()

    # Metodo para configurar la unidad experimental
    def getUnidadExperimental(self):
        return self.inputs

    # Metodo para configurar el trafico
    def configurarTrafico(self, tipo = 'normal'):
        nodos_claves = self.inputs.obtenerNodosClaves()
        if tipo == 'normal':
            h_c = self.net.get(nodos_claves[1])
            h_v = self.net.get(nodos_claves[2])
            self.trafico = TraficoNormal(h_c,h_v)
        elif tipo == 'ataque':
            h_a = self.net.get(nodos_claves[0])
            h_c = self.net.get(nodos_claves[1])
            h_v = self.net.get(nodos_claves[2])
            self.trafico = TraficoAtaque(h_a,h_c,h_v)


    def killTest(self):
        subprocess.call(["mn", "-c"])

    def killController(self):
        if self.inputs.getController() == 'ryu':
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if "ryu-manager" in proc.info['name']:
                    os.kill(proc.info['pid'], 9)

    def startTest(self):
        self.net.start()

    def endTest(self):
        self.net.stop()

    def startCLI(self):
        CLI(self.net)

    def pingAllTest(self):
        self.net.pingAll()
