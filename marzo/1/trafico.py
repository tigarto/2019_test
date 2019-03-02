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
            h_V.cmdPrint('kill %iperf')
            print("*** End iperf measure ***\n")

        else:
            info("Starting iperf server")
            h_V.cmdPrint('iperf', '-s', '&')
            h_C.cmd('iperf', '-c', h_V.IP(), '-i', intervalo, '-t ', tiempo, '>', filename)
            h_V.cmdPrint('kill %iperf')
            print("*** End iperf measure ***\n")

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
        tiempo_start = 3
        if h_src == None and h_dst == None and h_atk == None:
            h_C = self.src
            h_V = self.dst
            h_A = self.atk
            if self.tipo_ataque == 1:
                if filename == None:
                    info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                    process_attack = h_A.popen(['hping3', '--flood',
                                                '--rand-source',
                                                h_V.IP()])
                    if (process_attack != 0):
                        # sleep(tiempo_start)
                        info("Starting pings ***\n")
                        h_C.cmdPrint('ping -c', veces, '-i', intervalo, str(h_V.IP()))
                        info("End pings ***\n")
                        process_attack.kill()
                else:
                    info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                    process_attack = h_A.popen(['hping3', '--flood',
                                                '--rand-source',
                                                h_V.IP()])
                    if (process_attack != 0):
                        # sleep(tiempo_start)
                        info("Starting pings ***\n")
                        h_C.cmd('ping -c', veces, '-i', intervalo, str(h_V.IP()),'>',filename)
                        info("End pings ***\n")
                        process_attack.kill()
                        h_V.cmd('kill %iperf')

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
        tiempo_start = 3
        if h_src == None and h_dst == None and h_atk == None:
            h_C = self.src
            h_V = self.dst
            h_A = self.atk
        if self.tipo_ataque == 1:
            if filename == None:
                info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                process_attack = h_A.popen(['hping3', '--flood',
                                            '--rand-source',
                                            h_V.IP()])
                if process_attack != 0:
                    # sleep(tiempo_start)
                    info("Starting iperf server\n")
                    h_V.cmdPrint('iperf', '-s', '&')
                    #sleep(tiempo_start)
                    h_C.cmdPrint('iperf', '-c', h_V.IP(), '-i', intervalo, '-t ', tiempo)
                    print("*** End iperf measure ***\n")
            else:
                info("Launch attack: %s ---> %s\n" % (str(h_A.IP()), str(h_V.IP())))
                process_attack = h_A.popen(['hping3', '--flood',
                                            '--rand-source',
                                            h_V.IP()])
                if process_attack != 0:
                    # sleep(tiempo_start)
                    info("Starting iperf server\n")
                    h_V.cmdPrint('iperf', '-s', '&')
                    h_C.cmd('iperf', '-c', h_V.IP(), '-i', intervalo, '-t ', tiempo, '>', filename)
                    print("*** End iperf measure ***\n")

