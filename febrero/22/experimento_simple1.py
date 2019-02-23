import os
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from mininet.topo import Topo
import subprocess
from time import time, sleep
import psutil

"""

Proceso de test:
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
sudo python experimento.py

"""

class TopologiaExperimento(Topo):
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

def launchController():
    return_code = subprocess.call("gnome-terminal --command='./run_controller.sh'", shell=True)
    if return_code == 0:
        info('*** Controlador iniciado con exito\n')
    else:
        info('*** Falla en el inicio del controlador\n')


def launchNet():
    "Creacion de la red"
    net = Mininet(topo = TopologiaExperimento(),
                  switch=OVSSwitch,
                  build=False,
                  link=TCLink,
                  controller=RemoteController(name = 'c0',port=6653))
    info('*** Build the network\n')
    net.build()
    info('*** Arrancndo la red\n')
    net.start()
    net.iperf()
    #print(net.hosts)
    info('*** Deteniendo la red\n')
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    #launchController()
    return_code = subprocess.call("gnome-terminal --command='./run_controller.sh'", shell=True)
    sleep(5)
    """
    launchNet()
    info('*** Removiendo la red\n')
    subprocess.call("mn -c")
    """
    pid_hijo = os.fork()
    if pid_hijo == 0:
        #sleep(5)
        launchNet()
        info('*** Removiendo la red\n')
        subprocess.call(["mn", "-c"])
    

    else:
        os.wait()
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if "ryu-manager" in proc.info['name']:
                os.kill(proc.info['pid'], 9)

