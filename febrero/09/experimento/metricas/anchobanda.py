from mininet.net import Mininet
from mininet.log import info, setLogLevel
from time import time,sleep
from subprocess import Popen, PIPE
from select import poll, POLLIN
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink

class IperfMeasure(object):
    def __init__(self, hSrc = None, hDst = None, outfile = 'iperf_measure.out',t_total = 10, intervalo = 1):
        self.hSrc = hSrc
        self.hDst = hDst
        self.outfile = outfile
        self.t_total = t_total
        self.intervalo = intervalo

    def configHosts(self, hSrc , hDst):
        self.hSrc = hSrc
        self.hDst = hDst

    def medirBW(self):
        sleep(1)
        info("Starting Iperf: %s ---> %s\n"%(str(self.hSrc.IP()),str(self.hDst.IP())))
        p1 = self.hDst.popen(['iperf', '-s']) # Iniciando el servidor
        logfile = open(self.outfile, 'w')
        p2 = self.hSrc.popen(['iperf', '-c', str(self.hDst.IP()), '-i', str(self.intervalo),
                         '-t ' + str(self.t_total)], stdout=PIPE)

        for line in p2.stdout:
            # sys.stdout.write(line)
            logfile.write(line)
        p2.wait()
        logfile.close()
        info("*** End iperf measure ***\n")

    def printOutputFile(self):
        info("***Output of iperf: %s ---> %s ***\n\n"%(str(self.hSrc.IP()),str(self.hDst.IP())))
        lines = open(self.outfile).readlines()
        for l in lines:
            info("%s"%(l))
        info("\n")

    def formatFile(self,filename_csv = 'iperf_measure.csv'):
        fileout_csv = open(filename_csv,'w')
        lines = open(self.outfile).readlines()
        fileout_csv.writelines("Interval;Transfer;Bandwidth\n")
        for l in lines[6:len(lines)]:
            s = l.split()
            s[:2] = []
            if len(s) == 7:
                lw = s[0] + s[1] + ";" + s[3] + ";" + s[5] + "\n"
            else:
                lw = s[0] + ";" + s[2] + ";" + s[4] + "\n"
            fileout_csv.write(lw)
        fileout_csv.close()


class BWMeasureAttack(IperfMeasure):
    def __init__(self, C=None, A=None, V=None, ipps = None, outfile='iperf_attack_measure.out', t_total=10, intervalo=1):
        IperfMeasure.__init__(self,hSrc = A, hDst = V, outfile = outfile,t_total = t_total, intervalo = intervalo)
        self.hM = C
        self.ipps = ipps

    def configAttack(self,C,V,A,ipps):
        self.hM = C
        self.hDst = V
        self.hSrc = A
        self.ipps = ipps

    def medirBWAtaque(self):
        sleep(1)
        info("*** Starting iperf measure ***\n")
        p1 = self.hDst.popen(['iperf', '-s'])
        logfile = open(self.outfile, 'w')

        p2 = self.hM.popen(['iperf', '-c', str(self.hDst.IP()), '-i', str(self.intervalo),
                      '-t ' + str(self.t_total)], stdout=PIPE)
        p3 = self.hSrc.popen(['hping3', '-i', self.ipps,
                              '--rand-source',
                              self.hDst.IP()])
        for line in p2.stdout:
            # sys.stdout.write(line)
            logfile.write(line)
        p2.wait()
        logfile.close()
        #p3.kill()
        info("*** End iperf attack ***\n")

    def printOutputFile(self):
        info("***Output of iperf: %s ---> %s ***\n\n"%(str(self.hM.IP()),str(self.hDst.IP())))
        lines = open(self.outfile).readlines()
        for l in lines:
            info("%s"%(l))
        info("\n")



def test1():
    info('*** Create the file config \n')
    iperfM = IperfMeasure()


    "Create Simple topology example."
    net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
    # Initialize topology

    # Add containers
    h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
    h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
    h3 = net.addHost('h3', ip='10.0.0.3')  # Victima
    iperfM.configHosts(h2,h3)

    # Add switches
    info('*** Adding switches\n')
    sw1 = net.addSwitch('sw1', protocols='OpenFlow13')

    # Add links
    info('*** Creating links\n')
    net.addLink(h1, sw1, bw=100)
    net.addLink(h2, sw1, bw=100)
    net.addLink(h3, sw1, bw=100)

    # Build the network
    info('*** Build the network\n')
    net.build()

    info('*** Starting network\n')
    net.start()
    iperfM.medirBW()

    info('*** Stopping network')
    net.stop()
    iperfM.printOutputFile()
    #medida.formatFile()

def test2():
    info('*** Create the file config \n')
    iperfM = BWMeasureAttack()

    "Create Simple topology example."
    net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
    # Initialize topology

    # Add containers
    h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
    h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
    h3 = net.addHost('h3', ip='10.0.0.3')  # Victima
    iperfM.configAttack(h2,h3,h1,'u500')


    # Add switches
    info('*** Adding switches\n')
    sw1 = net.addSwitch('sw1', protocols='OpenFlow13')

    # Add links
    info('*** Creating links\n')
    net.addLink(h1, sw1, bw=100)
    net.addLink(h2, sw1, bw=100)
    net.addLink(h3, sw1, bw=100)

    # Build the network
    info('*** Build the network\n')
    net.build()

    info('*** Starting network\n')
    net.start()
    iperfM.medirBWAtaque()

    info('*** Stopping network')
    net.stop()
    iperfM.printOutputFile()
    iperfM.formatFile()

if __name__ == "__main__":
    setLogLevel('info')
    #test1()
    test2()