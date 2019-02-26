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


class Entradas:
    def __init__(self):
        self.ensayos = []

    def iperfTest(self,src,dst,fileOut = None):
        return {'BW':[src,dst,fileOut]}

    def pingTest(self,src,dst,fileOut = None):
        return {'ping': [src, dst, fileOut]}

    def agregarEnsayo(self,test):
        self.ensayos.append(test)

    def listarEnsayos(self):
        i = 1
        for e in self.ensayos:
            print(str(i) + '. [' + e.keys()[0] + ']: ' + e.values()[0][0] + '--' + e.values()[0][1])
            i+=1

    def eliminarEnsayos(self):
        self.ensayos = []

    def obtenerEnsayos(self):
        return self.ensayos


## Clase asociadad al controlador --- RYU ##

class RYU( Controller ):
    def __init__(self, name, ryuArgs, **kwargs):
        Controller.__init__(self, name,
                            command = '/usr/local/bin/ryu-manager',
                            cargs='--ofp-tcp-listen-port %s ' + ryuArgs,
                            **kwargs)

## Clase asociada a una topologia (simple para el caso) ##

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

## Clase asociada a la unidad experimental ##

class UnidadExperimental:
    def __init__(self, topo = None, controller = None):
        self.topo = topo
        self.controller = controller
        self.atacante = None
        self.victima = None
        self.cliente = None

    def setTopo(self,topo):
        self.topo = topo

    def setController(self,controller,appsController = 'simple_switch_13.py'):
        if controller == 'ryu':
            self.controller = RYU(name='c0',
                                  ryuArgs =appsController)

    def getTopo(self):
        return self.topo

    def getController(self):
        return self.controller

    def definirNodosClaves(self,A,C,V):
        self.atacante = A
        self.cliente = C
        self.victima = V

    def obtenerNodosClaves(self):
        return [self.atacante, self.cliente, self.victima]


## Clase asociada al experimento ##

class Experimento:
    def __init__(self):
        self.net = None
        self.inputs = None

    def configureParams(self,ue):
        self.inputs = ue
        self.net = Mininet( controller=ue.getController(),
                            switch=OVSSwitch,
                            build=False,
                            link=TCLink,
                            topo = ue.getTopo()
                          )
        self.net.build()

    def getUnidadExperimental(self):
        return self.inputs

    def killTopo(self):
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
        #self.net.start()
        self.net.pingAll()
        #self.net.start()

    def pingMeasure(self,
                    src_in = None,
                    dst_in = None,
                    veces = 4,
                    intervalo = 1,
                    filename = None):
        nodosClaves = self.inputs.obtenerNodosClaves()
        if filename == None:
            if src_in == None and dst_in == None:
                src = nodosClaves[1]
                dst = nodosClaves[2]
                #self.net.ping(src,dst)
                src = self.net.get(src)
                dst = self.net.get(dst)
            else:
                src = self.net.get(src_in)
                dst = self.net.get(dst_in)
            src.cmdPrint('ping -c',veces,'-i',intervalo,str(dst.IP()))
        else:
            if src_in == None and dst_in == None:
                src = nodosClaves[1]
                dst = nodosClaves[2]
                src = self.net.get(src)
                dst = self.net.get(dst)
            else:
                src = self.net.get(src_in)
                dst = self.net.get(dst_in)
            info("Starting Pings: %s ---> %s\n" % (str(src.IP()), str(dst.IP())))
            logfile = open(filename, 'w')
            p = src.popen(['ping', str(dst.IP()),
                                 '-i', str(intervalo),
                                 '-c', str(veces)],
                                 stdout=PIPE)
            for line in p.stdout:
                logfile.write(line)
            p.wait()
            logfile.close()
            info("End pings ***\n")

    def iperfTest(self, src_in=None, dst_in=None, veces=4, filename=None):
        if filename == None:
            nodosClaves = self.inputs.obtenerNodosClaves()
            if src_in == None and dst_in == None:
                self.net.iperf()
            else:
                src = self.net.get(src_in)
                dst = self.net.get(dst_in)
                self.net.iperf([src, dst])

    def iperfMeasure(self,
                     src_in=None,
                     dst_in=None,
                     intervalo=1,
                     tiempo = 10,
                     filename = 'salida.log'
                     ):
        nodosClaves = self.inputs.obtenerNodosClaves()
        if src_in == None and dst_in == None:
            src = nodosClaves[1]
            dst = nodosClaves[2]
            # self.net.ping(src,dst)
            src = self.net.get(src)
            dst = self.net.get(dst)
        else:
            src = self.net.get(src_in)
            dst = self.net.get(dst_in)
        logfile = open(filename, 'w')
        info("Starting Iperf: %s ---> %s\n" % (str(src.IP()), str(dst.IP())))
        p1 = dst.popen(['iperf', '-s'])  # Iniciando el servidor
        p2 = src.popen(['iperf', '-c', str(dst.IP()), '-i', str(intervalo),
                              '-t ' + str(tiempo)], stdout=PIPE)
        for line in p2.stdout:
            logfile.write(line)
        p2.wait()
        logfile.close()
        info("*** End iperf measure ***\n")



## Funciones de test ##

def test1():
    setLogLevel("debug")
    print ("Configuracion Unidad experimental")
    t1 = Topologia1()
    ue1 = UnidadExperimental()
    ue1.setTopo(t1)
    ue1.setController('ryu', 'simple_switch_13.py,ofctl_rest.py')
    print ("Configuracion del experimento")
    exp1 = Experimento()
    exp1.configureParams(ue1)
    exp1.startTest()
    exp1.startCLI()
    exp1.endTest()
    print ("Removiendo la topologia")
    exp1.killTopo()
    # print ("Removiendo el controlador")
    # exp1.killController()   # Si no se pone no se finaliza el controlador


def test2():
    # Configurando las entradas
    ent1 = Entradas()
    ent1.agregarEnsayo({'BW': ['h2', 'h3']})
    ent1.agregarEnsayo({'BW': ['h2', 'h1']})
    ent1.listarEnsayos() # Para cuando se tengan multiples ensayos
    test_iperf = ent1.agregarEnsayo('BW','h2', 'h3') # Caso con un solo ensayo


def test3():
    setLogLevel("info")
    print ("Configuracion Unidad experimental")
    t1 = Topologia1()
    ue1 = UnidadExperimental()
    ue1.setTopo(t1)
    ue1.setController('ryu', 'simple_switch_13.py,ofctl_rest.py')
    print ("Configuracion del experimento")
    exp1 = Experimento()
    exp1.configureParams(ue1)
    exp1.startTest()
    #exp1.pingAllTest()
    exp1.pingMeasure('h2','h3')
    #exp1.pingMeasure('h2', 'h3')
    exp1.pingMeasure('h2','h3',10,1,'test_ping.log')
    #exp1.iperfTest()
    #exp1.iperfTest('h2','h3')
    exp1.iperfMeasure('h2','h3')

    exp1.endTest()
    print ("Removiendo la topologia")
    exp1.killTopo()


if __name__ == "__main__":
    # test1()    # OK
    # test2()    # No empleado
    test3()      # OK











