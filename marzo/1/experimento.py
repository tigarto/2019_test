import os
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
import subprocess
from time import time, sleep
import psutil
from mininet.cli import CLI

# 
from trafico import TraficoAtaque, TraficoNormal
from prueba_clases import UnidadExperimental
from topologia import TopologiaPOX, TopologiaRyu
from controlador import RYU, POX

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

## Funciones de test ##

def test1():
    setLogLevel("debug")
    print ("Configuracion Unidad experimental")
    t1 = TopologiaRyu()
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
    t1 = TopologiaRyu()
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
    t1 = TopologiaRyu()
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

def test5():
    """ Prueba con ping normal """
    setLogLevel("info")
    info("Configuracion Unidad experimental")
    """ 1 -> Definicion de la topologia """
    t1 = Topologia1()
    ue1 = UnidadExperimental()
    ue1.setTopo(t1)
    ue1.definirNodosClaves(A = 'h1', C='h2', V='h3')  # Caso solo para trafico normal
    ue1.setController('ryu', 'simple_switch_13.py,ofctl_rest.py')
    info("Configuracion del experimento")
    """ 3. Confiracion del experimento """
    exp1 = Experimento()
    exp1.configureParams(ue1)
    exp1.configurarTrafico('ataque')
    """ 4. Inicio del experimento """
    exp1.startTest()
    exp1.pingAllTest()  # **************** Parece que es necesario que se de un arranque al controlador
                        # **************** para que aprenda las reglas antes del ataque.

    """ 5. Aplicacion de pruebas """
    exp1.trafico.pingMeasure()
    exp1.trafico.pingMeasure(filename='ping_ataque_test.log')
    """ 6. Fin del experimento """
    exp1.endTest()
    info("Removiendo la topologia\n")
    exp1.killTest()
    info("Removiendo el controlador\n")
    exp1.killController()  # Si no se pone no se finaliza el controlador

def test6():
    """ Prueba con ping normal """
    setLogLevel("info")
    info("Configuracion Unidad experimental")
    """ 1 -> Definicion de la topologia """
    t1 = TopologiaRyu()
    ue1 = UnidadExperimental()
    ue1.setTopo(t1)
    ue1.definirNodosClaves(A = 'h1', C='h2', V='h3')  # Caso solo para trafico normal
    ue1.setController('ryu', 'simple_switch_13.py,ofctl_rest.py')
    info("Configuracion del experimento")
    """ 3. Confiracion del experimento """
    exp1 = Experimento()
    exp1.configureParams(ue1)
    exp1.configurarTrafico('ataque')
    """ 4. Inicio del experimento """
    exp1.startTest()
    """ 5. Aplicacion de pruebas """
    # exp1.trafico.iperfMeasure()  # Si se lanza afecta la proxima medida.
    exp1.trafico.iperfMeasure(filename='iperf_ataque_test.log')
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
    # test4()    # Prueba con iperf normal (consola y archivo) - OK ** No se ve la cosa en pantalla
    # test5()    # Prueba con ping bajo ataque - Parece que OK
    test6()      # Prueba con iperf bajo ataque (consola y archivo parece que OK) - Nota: Solo hacer un caso pues el
                 # resultado se afecta.
