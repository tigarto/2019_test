import os
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from mininet.topo import Topo, SingleSwitchTopo
import subprocess
from time import time, sleep
import psutil
from mininet.cli import CLI
from subprocess import Popen, PIPE, STDOUT
from select import poll, POLLIN
import threading
import signal
from mininet.topolib import TreeTopo 
from controlador import RYU, POX
from unidadExperimental import UnidadExperimental
from mininet.link import TCLink


TIEMPO_ADICIONAL = 4

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
        self.timer = None
        Trafico.__init__(self, src = src, dst = dst)

    def pingMeasure(self,
                    h_src = None,
                    h_dst = None,
                    veces = 10,
                    intervalo = 1.0,
                    filename = None):

        h_C = h_src
        h_V = h_dst
        if h_src == None and h_dst == None:
            h_C = self.src
            h_V = self.dst
        if filename == None:
            info("Starting Pings: %s ---> %s\n" % (str(h_C.IP()), str(h_V.IP())))            
            h_C.cmdPrint('ping -c', veces, '-i', intervalo, str(h_V.IP()))
            info("End pings ***\n")
        else:
            info("Starting Pings: %s ---> %s\n" % (str(h_C.IP()), str(h_V.IP())))            
            logfile = open(filename, 'w')
            info("Open file: %s\n"%filename)
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
            # Cuando hay nombre de archivo
            info("Starting iperf server in %s\n"%(str(h_V.IP()))) 
            # Proceso hijo
            iperf_server_process = h_V.popen(['iperf', '-s'])
            if iperf_server_process != 0:
                # Proceso padre
                info("Starting iperf client in %s\n"%(str(h_C.IP())))
                h_C.cmdPrint('iperf', '-c', h_V.IP(), '-i', intervalo, '-t ', tiempo)
                iperf_server_process.kill()
                info("End iperf measure ***\n")
        else:
            info("Starting iperf server in %s\n"%(str(h_V.IP()))) 
            # Proceso hijo
            iperf_server_process = h_V.popen(['iperf', '-s'])
            if iperf_server_process != 0:
                info("Starting iperf client in %s\n"%(str(h_C.IP())))
                info("Open file: %s\n"%filename)
                h_C.cmd('iperf', '-c', h_V.IP(), '-i', intervalo, '-t ', tiempo, '>', filename)
                iperf_server_process.kill()                
                info("End iperf measure ***\n")
                

class TraficoAtaque(Trafico):
    def __init__(self, atk = None,src = None, dst = None, tipo_ataque = 1):
        Trafico.__init__(self, src = src, dst = dst)
        self.atk = atk
        self.tipo_ataque = tipo_ataque # 1. Flooding and spoofing
        self.timer = None

    def pingMeasure(self,
                    h_atk = None,
                    h_src = None,
                    h_dst = None,
                    veces = 10,
                    intervalo = 1.0,
                    filename = None):
        h_C = h_src
        h_V = h_dst
        h_A = h_atk
        if h_src == None and h_dst == None and h_atk == None:
            h_C = self.src
            h_V = self.dst
            h_A = self.atk
            if self.tipo_ataque == 1:
                if filename == None:
                    # Caso en el cual no se redirecciona a un archivo
                    info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                    # Proceso hijo que lanza el araque
                    process_attack = h_A.popen(['hping3', '--flood',
                                                '--rand-source',
                                                h_V.IP()])
                    if (process_attack != 0):
                        # Codigo del padre
                        info("Starting pings ***\n")
                        h_C.cmdPrint('ping -c', veces, '-i', intervalo, str(h_V.IP()))
                        info("End pings ***\n")
                        process_attack.kill()
                        info("End attack ***\n")
                else:
                    # Caso en el que se redirecciona la salida del ping a un archivo
                    info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                    # Proceso hijo que lanza el araque
                    process_attack = h_A.popen(['hping3', '--flood',
                                                '--rand-source',
                                                h_V.IP()])
                    if (process_attack != 0):
                        # Codigo del padre
                        info("Starting pings ***\n")
                        h_C.cmd('ping -c', veces, '-i', intervalo, str(h_V.IP()),'>',filename)
                        info("End pings ***\n")
                        process_attack.kill()
                        info("End attack ***\n")

    def iperfMeasure(self,
                        h_atk = None,
                        h_src = None,
                        h_dst = None,
                        intervalo = 1,
                        tiempo = 10,
                        filename = None
                        ):
            # Es obligatorio poner el nombre del archivo
            h_C = h_src
            h_V = h_dst
            h_A = h_atk
            if h_src == None and h_dst == None and h_atk == None:
                h_C = self.src
                h_V = self.dst
                h_A = self.atk
                if self.tipo_ataque == 1:
                    info("++++++ Ataque DoS por flooding y spoofing +++++\n")
                    if filename != None:
                        log = open(filename,'w')
                        info("Starting iperf server\n")                    
                        server_process = h_V.popen(['iperf', '-s'])  # Victima  (Servidor)
                        if server_process != 0:
                            info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                            attack_process = h_A.popen(['hping3', '--flood',
                                                    '--rand-source',
                                                    h_V.IP()])  # Atacante
                            if attack_process != 0:
                                # Iniciando cliente                                
                                info("Starting iperf client\n")
                                client_process = h_C.popen(['iperf', '-c',
                                                    str(h_V.IP()),'-i',str(intervalo),
                                                    '-t',str(tiempo)],stdout=log, stderr=log, shell=True)
                                if client_process != 0:
                                    self.timer = threading.Timer(tiempo + TIEMPO_ADICIONAL, self.killIperfClient, 
                                                                 args=[client_process,server_process,attack_process] )
                                    self.timer.start()
                                    self.timer.join()
                                info("Starting iperf measure\n")
                    else:
                        info("Es necesario colocar un nombre de archivo a la entrada para almacenar los resultados\n")
                        # Nota: Mirar si con cmdPrint se puede obtener el pid para killearlo como en el caso de Popen
                        # Puede que last pid sirva?

    def killIperfClient(self,p1,p2,p3):
        p1.kill()
        p2.kill()
        p3.kill()
        self.timer.cancel()
   

  


# https://www.linode.com/docs/networking/diagnostics/install-iperf-to-diagnose-network-speed-in-linux/



  


ue1 = UnidadExperimental(topo=SingleSwitchTopo(k = 3, bw = 100),controller=RYU('c0'))
ue1.definirNodosClaves('h1','h2','h3')

ue2 = UnidadExperimental(topo=SingleSwitchTopo(k = 3, bw = 100),controller=POX('c0'))
ue2.definirNodosClaves('h1','h2','h3')

class TopologiaTest(Topo):
    def __init__(self, bw = 100):
        # Initialize topology
        Topo.__init__(self)
        self.bw = bw
        h1 = self.addHost('h1', ip='10.0.0.1')  # Cliente
        h2 = self.addHost('h2', ip='10.0.0.2')  # Atacante
        h3 = self.addHost('h3', ip='10.0.0.3')  # Victima

        # Add switches
        info('*** Adding switches\n')
        s1 = self.addSwitch('s1', protocols='OpenFlow13')

        # Add links
        info('*** Creating links\n')
        self.addLink(h1, s1, bw = self.bw)
        self.addLink(h2, s1, bw = self.bw)
        self.addLink(h3, s1, bw = self.bw)

ue3 = UnidadExperimental(topo=TopologiaTest(100),controller=RYU('c0'))
ue3.definirNodosClaves('h1','h2','h3')

ue4 = UnidadExperimental(topo=TopologiaTest(100),controller=POX('c0'))
ue4.definirNodosClaves('h1','h2','h3')

def test_ping_normal(ue,nombreArchivo = None):
    # Parametros de la unidad experimental
    setLogLevel("info")
    info("Configurando unidad experimental\n")
    info("Configurando trafico normal\n")
    info("Configurando la red\n")
    net = Mininet(topo = ue.getTopo(),controller=ue.getController(),build=False)
    net.build()
    # Configurando clase asociada al trafico
    info("Configurando clase asociada al trafico\n")    
    [A,C,V] = ue.obtenerNodosClaves()
    # ---- info("%s %s %s\n"%(A,C,V))
    C = net.get(C)
    V = net.get(V)
    t_normal = TraficoNormal(C,V)
    # Arrancando la red
    net.start()
    net.pingAll()
    # t_normal.pingMeasure() # Mostrando salida en pantalla
    t_normal.pingMeasure(filename = nombreArchivo) # Llevando salida a un archivo
    CLI(net)
    net.stop()

def test_iperf_normal(ue,nombreArchivo = None):
    # Parametros de la unidad experimental
    setLogLevel("info")
    info("Configurando unidad experimental\n")
    info("Configurando trafico normal\n")
    info("Configurando la red\n")
    net = Mininet(topo = ue.getTopo(), controller=ue.getController(), link=TCLink ,build=False)
    net.build()
    # Configurando clase asociada al trafico
    info("Configurando clase asociada al trafico\n")    
    [A,C,V] = ue.obtenerNodosClaves()
    # ---- info("%s %s %s\n"%(A,C,V))
    C = net.get(C)
    V = net.get(V)
    t_normal = TraficoNormal(C,V)
    # Arrancando la red
    net.start()
    net.pingAll()
    t_normal.iperfMeasure(filename = nombreArchivo) # Llevando salida a un archivo
    CLI(net)
    net.stop()


def test_ping_ataque(ue,nombreArchivo = None):
    # Parametros de la unidad experimental
    setLogLevel("info")
    info("Configurando unidad experimental\n")
    info("Configurando trafico normal\n")
    info("Configurando la red\n")
    net = Mininet(topo = ue.getTopo(),controller=ue.getController(),build=False)
    net.build()
    # Configurando clase asociada al trafico
    info("Configurando clase asociada al trafico\n")    
    [A,C,V] = ue.obtenerNodosClaves()
    A = net.get(A)
    C = net.get(C)
    V = net.get(V)
    t_ataque = TraficoAtaque(A,C,V)
    # Arrancando la red
    net.start()
    net.pingAll()
    t_ataque.pingMeasure() # Mostrando salida en pantalla
    t_ataque.pingMeasure(filename = nombreArchivo) # Llevando salida a un archivo
    CLI(net)
    net.stop()

def test_iperf_ataque(ue,nombreArchivo = None):
    # Parametros de la unidad experimental
    setLogLevel("info")
    info("Configurando unidad experimental\n")
    info("Configurando trafico normal\n")
    info("Configurando la red\n")
    net = Mininet(topo = ue.getTopo(), controller=ue.getController(), link=TCLink ,build=False)
    net.build()
    # Configurando clase asociada al trafico
    info("Configurando clase asociada al trafico\n")    
    [A,C,V] = ue.obtenerNodosClaves()
    A = net.get(A)
    C = net.get(C)
    V = net.get(V)
    t_ataque = TraficoAtaque(A,C,V)
    # Arrancando la red
    net.start()
    net.pingAll()
    #t_ataque.iperfMeasure() # Mostrando salida en pantalla
    t_ataque.iperfMeasure(filename = nombreArchivo) # Llevando salida a un archivo
    CLI(net)
    net.stop()

    
def test_iperf_mix_sin_timer(ue,nombreArchivo = None):
    # Parametros de la unidad experimental
    setLogLevel("info")
    info("Configurando unidad experimental\n")
    info("Configurando trafico normal\n")
    info("Configurando la red\n")
    net = Mininet(topo = ue.getTopo(), controller=ue.getController(), link=TCLink ,build=False)
    net.build()
    # Configurando clase asociada al trafico
    info("Configurando clase asociada al trafico\n")    
    [A,C,V] = ue.obtenerNodosClaves()
    A = net.get(A)
    C = net.get(C)
    V = net.get(V)
    #t_ataque = TraficoAtaque(A,C,V)
    # Arrancando la red
    net.start()
    net.pingAll()
    A.cmdPrint('hping3', '--flood','--rand-source',V.IP(),'&')
    net.iperf(hosts = [C,V], seconds = 10)
    A.cmdPrint("kill %hping3")
    #t_ataque.iperfMeasure() # Mostrando salida en pantalla
    #t_ataque.iperfMeasure(filename = nombreArchivo) # Llevando salida a un archivo
    CLI(net)
    net.stop()

def test_iperf_mix_con_timer(ue,nombreArchivo = None, i = 1, t = 10):

    def killAlarma(A,C,V):
        info("Hola alarma\n")
        C.cmdPrint("ps|grep iperf &")
        A.cmdPrint("kill %hping3")
        A.cmdPrint("ps")
        V.cmdPrint("kill -9 %iperf &")
        C.cmdPrint("kill -9 %iperf &")
        info("Chao alarma\n")


    def killAlarma2(p):
        info("Hola alarma\n")
        os.kill(p.pid, signal.SIGTERM)
        info("Chao alarma\n")


    def killAlarma3(p1,p2,p3):
        info("Hola alarma\n")
        os.kill(p1.pid, signal.SIGTERM)
        os.kill(p2.pid, signal.SIGTERM)
        os.kill(p3.pid, signal.SIGTERM)
        info("Chao alarma\n")
        

    


    # Parametros de la unidad experimental
    # https://crashcourse.housegordon.org/python-subprocess.html
    setLogLevel("info")
    info("Configurando unidad experimental\n")
    info("Configurando trafico normal\n")
    info("Configurando la red\n")
    net = Mininet(topo = ue.getTopo(), controller=ue.getController(), link=TCLink ,build=False)
    net.build()
    # Configurando clase asociada al trafico
    info("Configurando clase asociada al trafico\n")    
    [A,C,V] = ue.obtenerNodosClaves()
    A = net.get(A)
    C = net.get(C)
    V = net.get(V)
    #t_ataque = TraficoAtaque(A,C,V)
    # Arrancando la red
    net.start()
    net.pingAll()
    log = open(nombreArchivo,"w")
    info("*** Iniciando el servidor iperf ***\n")
    server_process = V.popen(['iperf','-s'])
    if server_process != 0:
        info("*** Lanzando el ataque ***\n")  
        atack_process = A.popen(['hping3', '--flood','--rand-source',str(V.IP())])
        if atack_process != 0:
            info("*** Lanzando el cliente iperf ***\n")
            client_process = C.popen(['iperf', '-c', str(V.IP()),'-i',str(i),
                              '-t',str(t)],stdout=log, stderr=log, shell=True)
            if client_process != 0:
                #timer = threading.Timer(10, killAlarma, args=[A,C,V] )
                #timer = threading.Timer(10, killAlarma2, args=[client_process])
                timer = threading.Timer(t + 2, killAlarma3, 
                                        args=[atack_process,client_process,server_process])
                timer.start()
                #net.iperf(hosts = [C,V], seconds = 10)
                timer.join()
                #A.cmdPrint("kill %hping3")
                #t_ataque.iperfMeasure() # Mostrando salida en pantalla
                #t_ataque.iperfMeasure(filename = nombreArchivo) # Llevando salida a un archivo
                log.close()
                CLI(net)
                net.stop()



if __name__ == "__main__":
    # test_ping_normal(ue1,'ping_normal_ryu.log')
    # test_ping_normal(ue2,'ping_normal_pox.log')
    # test_ping_ataque(ue1,'ping_ataque_ryu.log')
    # test_ping_ataque(ue2,'ping_ataque_pox.log')
    # test_iperf_normal(ue3,'iperf_normal_ryu.log')
    # test_iperf_normal(ue4,'iperf_normal_pox.log')
    # test_iperf_ataque(ue3,'iperf_ataque_ryu.log')
    # test_iperf_ataque(ue4,'iperf_ataque_pox.log')
    # test_iperf_mix_con_timer(ue3,"salida_ryu.log")
    test_iperf_mix_con_timer(ue4,"salida_pox.log")



    







