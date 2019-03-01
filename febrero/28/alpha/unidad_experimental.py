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

## Clase asociada al trafico ##

class Trafico:
    # Se inicia objetos tipo nodo
    def __init__(self, src = None, dst = None):
        self.src = src
        self.dst = dst

    def obtenerNodoFuente(self):
        return self.src

    def obtenerNodoDestino(self):
        return self.dst

class TraficoNormal(Trafico):
    def __init__(self, src = None, dst = None):
        Trafico.__init__(self, src = src, dst = dst)

    def pingMeasure(self,
                    h_src = None,
                    h_dst = None,
                    veces=4,
                    intervalo=1,
                    filename=None):

        h_C = h_src
        h_V = h_dst
        if h_src == None and h_dst == None:
            h_C = self.src
            h_V = self.src
        if filename == None:
            h_C.cmdPrint('ping -c', veces, '-i', intervalo, str(h_V.IP()))
            info("End pings ***\n")
        else:
            info("Starting Pings: %s ---> %s\n" % (str(h_C.IP()), str(h_V.IP())))
            logfile = open(filename, 'w')
            ping_process = h_C.popen(['ping', str(h_V.IP()),
                           '-i', str(intervalo),
                           '-c', str(veces)],
                          stdout=PIPE)
            for line in ping_process.stdout:
                logfile.write(line)
            ping_process.wait()
            logfile.close()
            info("End pings ***\n")

    def iperfMeasure(self,
                     h_src = None,
                     h_dst = None,
                     intervalo=1,
                     tiempo=10,
                     filename=None
                     ):
        h_C = h_src
        h_V = h_dst
        if h_src == None and h_dst == None:
            h_C = self.src
            h_V = self.dst
        if filename == None:
            info("Starting iperf server\n")
            h_V.cmdPrint('iperf', '-s', '&')
            h_C.cmdPrint('iperf', '-c', h_V.IP(), '-i', intervalo, '-t ', tiempo)
            print("*** End iperf measure ***\n")

        else:
            info("Starting iperf server")
            h_V.cmdPrint('iperf', '-s', '&')
            h_C.cmd('iperf', '-c', h_V.IP(), '-i', intervalo, '-t ', tiempo, '>', filename)
            print("*** End iperf measure ***\n")


            """
            info("Starting iperf server")
            logfile = open(filename, 'w')
            iperf_process_server = h_V.popen(['iperf', '-s'])  # Iniciando el servidor

            if iperf_process_server != 0:
                info("Starting Iperf: %s ---> %s\n" % (str(h_C.IP()), str(h_V.IP())))
                iperf_process_client = h_C.popen(['iperf', '-c', str(h_V.IP()),
                                                  '-i', str(intervalo),
                                                  '-t ' + str(tiempo)],
                                                 stdout=PIPE)
                if iperf_process_client == 0:
                    for line in iperf_process_client.stdout:
                        logfile.write(line)
                    logfile.close()
                else:
                    iperf_process_client.wait()
                    iperf_process_server.kill()
                    info("*** End iperf measure ***\n")
                    
            """



class TraficoAtaque(Trafico):
    def __init__(self, atk = None,src = None, dst = None, tipo_ataque = 1):
        Trafico.__init__(self, src = src, dst = dst)
        self.atk = atk
        self.tipo_ataque = tipo_ataque # 1. Flooding and spoofing

    def pingMeasure(self,
                    h_atk = None,
                    h_src = None,
                    h_dst = None,
                    veces=4,
                    intervalo=1,
                    filename=None):
        h_C = h_src
        h_V = h_dst
        h_A = h_atk
        if h_src == None and h_dst == None:
            h_C = self.src
            h_V = self.dst
            h_A = self.atk
        if filename == None:
            if self.tipo_ataque == 1:
                process_attack = h_A.popen(['hping3', '--flood',
                              '--rand-source',
                              h_V.IP()])
                if process_attack == 0:
                    info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                else:
                    ping_process = h_C.popen(['ping', str(h_V.IP()),
                                              '-i', str(intervalo),
                                              '-c', str(veces)])
                    if ping_process != 0:
                        ping_process.wait()
                        process_attack.kill()
            else:
                logfile = open(filename, 'w')
                process_attack = h_A.popen(['hping3', '--flood',
                                            '--rand-source',
                                            h_V.IP()])
                if process_attack == 0:
                    info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                else:
                    info("Starting Pings: %s ---> %s\n" % (str(h_C.IP()), str(h_V.IP())))
                    ping_process = h_C.popen(['ping', str(h_V.IP()),
                                  '-i', str(intervalo),
                                  '-c', str(veces)],
                                 stdout=PIPE)
                    if ping_process == 0:

                        for line in ping_process.stdout:
                            logfile.write(line)
                        logfile.close()
                        info("End pings ***\n")
                    else:
                        ping_process.wait()
                        process_attack.kill()
                        info("End attack ***\n")

    def iperfMeasure(self,
                     h_atk=None,
                     h_src = None,
                     h_dst = None,
                     intervalo=1,
                     tiempo=10,
                     filename=None
                     ):
        h_C = h_src
        h_V = h_dst
        h_A = h_atk
        if h_src == None and h_dst == None:
            h_C = self.src
            h_V = self.dst
            h_A = self.atk
        if filename == None:
            if self.tipo_ataque == 1:
                process_attack = h_A.popen(['hping3', '--flood',
                              '--rand-source',
                              h_V.IP()])
                if process_attack == 0:
                    info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                else:
                    iperf_process_server = h_V.popen(['iperf', '-s'])  # Iniciando el servidor
                    if iperf_process_server == 0:
                        info("Starting iperf server")
                        iperf_process_client = h_C.popen(['iperf', '-c', str(h_V.IP()),
                                                          '-i', str(intervalo),
                                                          '-t ' + str(tiempo)])
                        if iperf_process_client == 0:
                            info("Starting Iperf: %s ---> %s\n" % (str(h_C.IP()), str(h_V.IP())))
                        else:
                            iperf_process_client.wait()
                            iperf_process_server.kill()
                            process_attack.kill()
                            info("*** End iperf attack measure ***\n")
        else:
            if self.tipo_ataque == 1:
                process_attack = h_A.popen(['hping3', '--flood',
                              '--rand-source',
                              h_V.IP()])
                if process_attack == 0:
                    info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                else:
                    iperf_process_server = h_V.popen(['iperf', '-s'])  # Iniciando el servidor
                    logfile = open(filename, 'w')
                    if iperf_process_server == 0:
                        info("Starting iperf server")
                        iperf_process_client = h_C.popen(['iperf', '-c', str(h_V.IP()),
                                                          '-i', str(intervalo),
                                                          '-t ' + str(tiempo)],
                                                         stdout=PIPE)
                        if iperf_process_client == 0:
                            info("Starting Iperf: %s ---> %s\n" % (str(h_C.IP()), str(h_V.IP())))
                            for line in iperf_process_client.stdout:
                                logfile.write(line)
                            logfile.close()
                        else:
                            iperf_process_client.wait()
                            iperf_process_server.kill()
                            process_attack.kill()
                            info("*** End iperf attack measure ***\n")


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

    def definirNodosClaves(self,A = None,C = None ,V = None):
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
        print(nodos_claves)
        if tipo == 'normal':
            nodos_claves = self.inputs.obtenerNodosClaves()
            h_c = self.net.get(nodos_claves[1])
            h_v = self.net.get(nodos_claves[2])
            print (type(h_c))
            print("----------------------------------------------------")
            self.trafico = TraficoNormal(h_c,h_v)

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
    exp1.configurarTrafico()  # Se deduce de la unidad experimental
    exp1.startTest()
    exp1.startCLI()
    exp1.endTest()
    print ("Removiendo la topologia")
    exp1.killTest()
    print ("Removiendo el controlador")
    exp1.killController()   # Si no se pone no se finaliza el controlador

def test2():
    setLogLevel("info")
    info("Configuracion Unidad experimental")
    """ 1 -> Definicion de la topologia """
    t1 = Topologia1()
    ue1 = UnidadExperimental()
    ue1.setTopo(t1)
    ue1.definirNodosClaves('h1','h2','h3') # Caso solo para trafico normal
    ue1.setController('ryu', 'simple_switch_13.py,ofctl_rest.py')
    """ 3. Confiracion del experimento """
    exp1 = Experimento()
    exp1.configureParams(ue1)

    """ 4. Inicio del experimento """
    exp1.startTest()
    """ 5. Aplicacion de pruebas """
    exp1.pingAllTest()
    """ 6. Fin del experimento """
    exp1.endTest()
    info("Removiendo la topologia\n")
    exp1.killTest()
    info("Removiendo el controlador\n")
    exp1.killController()  # Si no se pone no se finaliza el controlador

def test3():
    """ Prueba con ping normal """
    setLogLevel("info")
    info("Configuracion Unidad experimental")
    """ 1 -> Definicion de la topologia """
    t1 = Topologia1()
    ue1 = UnidadExperimental()
    ue1.setTopo(t1)
    ue1.definirNodosClaves(C='h2', V='h3')  # Caso solo para trafico normal
    ue1.setController('ryu', 'simple_switch_13.py,ofctl_rest.py')
    info("Configuracion del experimento")
    """ 3. Confiracion del experimento """
    exp1 = Experimento()
    exp1.configureParams(ue1)
    exp1.configurarTrafico('normal')
    """ 4. Inicio del experimento """
    exp1.startTest()
    """ 5. Aplicacion de pruebas """
    exp1.trafico.pingMeasure()
    exp1.trafico.pingMeasure(filename='ensayo_ping.log')
    """ 6. Fin del experimento """
    exp1.endTest()
    info("Removiendo la topologia\n")
    exp1.killTest()
    info("Removiendo el controlador\n")
    exp1.killController()  # Si no se pone no se finaliza el controlador


def test4():
    """ Prueba con ping normal """
    setLogLevel("info")
    info("Configuracion Unidad experimental")
    """ 1 -> Definicion de la topologia """
    t1 = Topologia1()
    ue1 = UnidadExperimental()
    ue1.setTopo(t1)
    ue1.definirNodosClaves(C='h2', V='h3')  # Caso solo para trafico normal
    ue1.setController('ryu', 'simple_switch_13.py,ofctl_rest.py')
    info("Configuracion del experimento")
    """ 3. Confiracion del experimento """
    exp1 = Experimento()
    exp1.configureParams(ue1)
    exp1.configurarTrafico('normal')
    """ 4. Inicio del experimento """
    exp1.startTest()
    """ 5. Aplicacion de pruebas """
    exp1.trafico.iperfMeasure()
    exp1.trafico.iperfMeasure(filename='iperf_normal_test.log')
    """ 6. Fin del experimento """
    exp1.endTest()
    info("Removiendo la topologia\n")
    exp1.killTest()
    info("Removiendo el controlador\n")
    exp1.killController()  # Si no se pone no se finaliza el controlador


if __name__ == "__main__":
    # test1()    # OK
    # test2()    # OK
    # test3()    # Prueba con ping normal (consola y archivo) - OK
    test4()









