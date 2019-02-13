from metricas.tiempo import PingMeasure, PingMeasureAttack
from metricas.anchobanda import BWMeasureAttack, IperfMeasure
import os
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from time import time,sleep
from subprocess import Popen, PIPE, STDOUT
from select import poll, POLLIN
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
CLASES ASOCIADAS AL EXPERIMENTO
"""

class Experimento(object):
    def __init__(self, desc = None, rep = 1, dirName = 'experimentos_ping'):
        self.descripcion = desc
        self.nReplicas = rep
        self.dirName = dirName
        #self.generateDir()

    def generateDir(self):
        if not os.path.exists(self.dirName):
            if '/' in self.dirName:
                os.makedirs(self.dirName)
            else:
                os.mkdir(self.dirName)
            print("Directory ", self.dirName, " Created ")
        else:
            print("Directory ", self.dirName, " already exists")

    def asignarDirName(self,dirName):
        self.dirName = dirName

    def crearNombresArchivos(self, filename):
        full_names = []
        full_name = os.path.dirname(os.path.abspath(__file__)) + "/" + self.dirName + "/" + filename
        print full_name
        if self.nReplicas == 1:
            full_names.append(full_name)
        else:
            partes_nombre = filename.split('.')
            for i in range(1,self.nReplicas + 1):
                filename = partes_nombre[0] + "_rep-" + str(i) + "." + partes_nombre[1]
                full_name = os.path.dirname(os.path.abspath(__file__)) + "/" + self.dirName + "/" + filename
                full_names.append(full_name)
        return full_names

class ExperimentoPing(Experimento):
    def __init__(self, desc = None, rep = 1, dirName = 'experimentos', tiempo = 10, tasaAtaque = None):
        Experimento.__init__(self, desc, rep, dirName)
        self.tiempo = tiempo
        self.tasaAtaque = tasaAtaque

    def medir(self,filename):
        print "Iniciando el experimento"
        list_files = self.crearNombresArchivos(filename)
        if self.tasaAtaque == None:
            for f in list_files:
                medida = PingMeasure(outfile=f, t_total=self.tiempo, intervalo=1)
                net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
                net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
                h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
                h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
                h3 = net.addHost('h3', ip='10.0.0.3')  # Victima
                medida.configHosts(h2, h3)
                sw1 = net.addSwitch('sw1', protocols='OpenFlow13')
                net.addLink(h1, sw1, bw=100)
                net.addLink(h2, sw1, bw=100)
                net.addLink(h3, sw1, bw=100)
                net.build()
                net.start()
                medida.medir()
                net.stop()
                medida.printOutputFile()

        else:
            for f in list_files:
                medida = PingMeasureAttack(outfile=f, t_total=self.tiempo, intervalo= 1)
                net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
                net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
                h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
                h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
                h3 = net.addHost('h3', ip='10.0.0.3')  # Victima
                medida.configAttack(h2, h3, h1, self.tasaAtaque)
                sw1 = net.addSwitch('sw1', protocols='OpenFlow13')
                net.addLink(h1, sw1, bw=100)
                net.addLink(h2, sw1, bw=100)
                net.addLink(h3, sw1, bw=100)
                net.build()
                net.start()
                medida.medirAtaque()
                net.stop()
                medida.printOutputFile()

class ExperimentoIperf(Experimento):
    def __init__(self, desc = None, rep = 1, dirName = 'experimentos_iperf', tiempo = 10, tasaAtaque = None):
        Experimento.__init__(self, desc, rep, dirName)
        self.tiempo = tiempo
        self.tasaAtaque = tasaAtaque

    def medir(self,filename):
        print "Iniciando el experimento"
        list_files = self.crearNombresArchivos(filename)
        if self.tasaAtaque == None:
            for f in list_files:
                medida = IperfMeasure(outfile=f, t_total=self.tiempo, intervalo=1)
                net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
                net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
                h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
                h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
                h3 = net.addHost('h3', ip='10.0.0.3')  # Victima
                medida.configHosts(h2, h3)
                sw1 = net.addSwitch('sw1', protocols='OpenFlow13')
                net.addLink(h1, sw1, bw=100)
                net.addLink(h2, sw1, bw=100)
                net.addLink(h3, sw1, bw=100)
                net.build()
                net.start()
                medida.medirBW()
                net.stop()
                medida.printOutputFile()
        else:
            for f in list_files:
                medida = BWMeasureAttack(outfile=f, t_total=self.tiempo, intervalo=1)
                net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
                net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
                h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
                h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
                h3 = net.addHost('h3', ip='10.0.0.3')  # Victima
                medida.configAttack(h2,h3,h1,self.tasaAtaque)
                sw1 = net.addSwitch('sw1', protocols='OpenFlow13')
                net.addLink(h1, sw1, bw=100)
                net.addLink(h2, sw1, bw=100)
                net.addLink(h3, sw1, bw=100)
                net.build()
                net.start()
                medida.medirBWAtaque()
                net.stop()
                medida.printOutputFile()


"""
FUNCIONES DE TEST
"""

def testPingNormal():
    print "Test clase Experimento"
    e = ExperimentoPing(rep = 3)
    e.generateDir()
    e.medir("pings.dat")

def testPingAtaque():
    print "Test clase Experimento"
    e = ExperimentoPing(rep = 3, tasaAtaque = 'u500')
    e.generateDir()
    e.medir("pings_ataque.dat")

def testIperfNormal():
    print "Test clase Experimento"
    e = ExperimentoIperf(rep = 3)
    e.generateDir()
    e.medir("iperfs.dat")

def testIperfAtaque():
    print "Test clase Experimento"
    e = ExperimentoIperf(rep = 3, tasaAtaque = 'u500', tiempo = 100)
    e.generateDir()
    e.medir("iperfs_ataque.dat")

"""
PROGRAMA QUE EJECUTA EL MAIN DEL EXPERIMENTO
"""

if __name__ == "__main__":
    setLogLevel('info')
    parametros_experimento = {
        'normal':None,
        '2kpps':'u500',
        '4kpps':'u250',
        '6kpps':'u166',
        '8kpps':'u125',
        '10kpps':'u100'     
    }
    num_replicas = 1
    t_total = 50
    # Generando los directorios para las pruebas
    for k in parametros_experimento:
        sleep(1)
        dirOut = dirName = 'salidas/' + k
        eb = Experimento(rep = num_replicas, dirName = dirOut + '/ping')
        eb.generateDir()
        eb.asignarDirName(dirOut + '/iperf')
        eb.generateDir()
        if k == 'normal':
            e = ExperimentoPing(rep = num_replicas)
            e.asignarDirName(dirOut + '/ping/')
            e.medir('ping' + k + '.out')
            e = ExperimentoIperf(rep = num_replicas, tiempo = t_total)
            e.asignarDirName(dirOut + '/iperf/')
            e.medir('iperf' + k + '.out')
        else:
            e = ExperimentoPing(rep = num_replicas, tasaAtaque = parametros_experimento[k], tiempo = t_total)
            e.asignarDirName(dirOut + '/ping/')
            e.medir('ping_ataque_' + k + '.out')
            e = ExperimentoIperf(rep = num_replicas, tasaAtaque = parametros_experimento[k], tiempo = t_total)
            e.asignarDirName(dirOut + '/iperf/')
            e.medir('iperf_ataque_' + k + '.out')

    
        


        




	



