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


class Metrica:
    def __init__(self):
        self.comando = []

    def addCommand(self,comando):
        self.comando.append(comando)

class Topologia1(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        h1 = self.addHost('h1', ip='10.0.0.1')  # Cliente
        h2 = self.addHost('h2', ip='10.0.0.2')  # Atacante
        h3 = self.addHost('h3', ip='10.0.0.3')  # Victima

        # Add switches
        info('*** Adding switches\n')
        sw1 = self.addSwitch('sw1', protocols='OpenFlow13')

        # Add links
        info('*** Creating links\n')
        self.addLink(h1, sw1, bw=100)
        self.addLink(h2, sw1, bw=100)
        self.addLink(h3, sw1, bw=100)

class UnidadExperimental:
    def __init__(self, topo = None, controller = None):
        self.topo = topo
        self.controller = controller
        self.atacante = None
        self.victima = None
        self.cliente = None

    def setTopo(self,topo):
        self.topo = topo

    def setController(self,controller):
        self.controller = controller

    def getTopo(self):
        return self.topo

    def getController(self):
        return self.controller

    def definirNodosClaves(self,A,C,V):
        self.atacante = A
        self.cliente = C
        self.victima = V



class Experimento:
    def __init__(self):
        self.net = None
        self.inputs = None

    def configureParams(self,ue):
        self.inputs = ue
        if ue.getController() == 'ryu':
            self.net = Mininet(
                                controller=RemoteController(name = 'c0',port=6653),
                                switch=OVSSwitch,
                                build=False,
                                link=TCLink,
                                topo = ue.getTopo()
                              )
            self.net.build()

    def getUnidadExperimental(self):
        return self.inputs


    def launchController(self):
        if self.inputs.getController() == 'ryu':
            return_code = subprocess.call("gnome-terminal --command='./run_ryu.sh'", shell=True)
            if return_code == 0:
                info('*** Controlador iniciado con exito\n')
            else:
                info('*** Falla en el inicio del controlador\n')

    def killTopo(self):
        subprocess.call(["mn", "-c"])

    def killController(self):
        if self.inputs.getController() == 'ryu':
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if "ryu-manager" in proc.info['name']:
                    os.kill(proc.info['pid'], 9)

    def launchExperiment(self):
        self.launchController()
        sleep(3)
        self.net.start()
        CLI(self.net)
        self.net.stop()





if __name__ == "__main__":
    setLogLevel("info")
    print ("Configuracion Unidad experimental")
    t1 = Topologia1()
    ue1 = UnidadExperimental()
    ue1.setTopo(t1)
    ue1.setController('ryu')
    print ("Configuracion del experimento")
    exp1 = Experimento()
    exp1.configureParams(ue1)
    exp1.launchExperiment()
    print ("Removiendo la topologia")
    exp1.killTopo()
    print ("Removiendo el controlador")
    exp1.killController()   # Si no se pone no se finaliza el controlador








