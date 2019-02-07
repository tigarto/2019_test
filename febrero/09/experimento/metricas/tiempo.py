from mininet.net import Mininet
from mininet.log import info, setLogLevel
from time import time,sleep
from subprocess import Popen, PIPE, STDOUT
from select import poll, POLLIN
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink


class PingMeasure(object):
    def __init__(self, hSrc = None, hDst = None, outfile = 'ping_measure.out',t_total = 10, intervalo = 1):
        self.__hSrc = hSrc
        self.__hDst = hDst
        self.__outfile = outfile
        self.__t_total = t_total
        self.__intervalo = intervalo

    def configHosts(self, hSrc , hDst):
        self.__hSrc = hSrc
        self.__hDst = hDst

    def getHosts(self):
        return [self.__hSrc,self.__hDst]

    def getFileName(self):
        return self.__outfile

    def getPingParameters(self):
        return [self.__t_total, self.__intervalo]

    def medir(self):
        info("Starting Pings: %s ---> %s\n"%(str(self.__hSrc.IP()),str(self.__hDst.IP())))
        logfile = open(self.__outfile, 'w')
        p = self.__hSrc.popen(['ping', str(self.__hDst.IP()),
                               '-i', str(self.__intervalo),
                               '-c', str(self.__t_total)],
                              stdout=PIPE)
        for line in p.stdout:
            logfile.write(line)
        p.wait()
        logfile.close()
        info("End pings ***\n")

    def printOutputFile(self):
        info("***Output of ping: %s ---> %s ***\n\n"%(str(self.__hSrc.IP()),str(self.__hDst.IP())))
        lines = open(self.__outfile).readlines()
        for l in lines:
            info("%s"%(l))
        info("\n")

    def getPacketInfo(self):
        lines = open(self.__outfile).readlines()
        line = lines[-2]
        s = line.split(', ')
        p_tx = int(int(s[0].split()[0]))
        p_rx = int(s[1].split()[0])
        p_loss =float(s[2].split()[0].replace('%', ''))
        time =float(s[3].split()[1].replace('ms', ''))
        return [p_tx, p_rx, p_loss, time]

    def formatFile(self,filename_csv = 'ping_measure.csv'):
        fileout_csv = open(filename_csv,'w')
        lines = open(self.__outfile).readlines()
        fileout_csv.writelines("icmp_seq;ttl;time\n")
        for l in lines[1:len(lines) - 4]:
            s = l.split()
            fileout_csv.write(s[0] + ";" + s[4].split("=")[1] + ";" +s[6].split("=")[1] + "\n")
        fileout_csv.close()

class PingMeasureAttack(PingMeasure):
    def __init__(self, C=None, A=None, V=None, ipps = None, outfile='ping_measure.out', t_total=10, intervalo=1):
        PingMeasure.__init__(self,A, V, outfile, t_total, intervalo)
        self.__hM = C
        self.__ipps = ipps

    def configAttack(self,C,V,A,ipps):
        self.__hM = C
        self.__hDst = V
        self.__hSrc = A
        self.__ipps = ipps

    def getHosts(self):
        return [self.__hSrc,self.__hDst,self.__hM]

    def medirAtaque(self):
        logfile = open(self.getFileName(), 'w')
        [A,V,C] = self.getHosts()
        info("Launch attack: %s ---> %s\n" % (str(A.IP()), str(V.IP())))
        p1 = A.popen(['hping3', '-i', self.__ipps,
                                '--rand-source',
                                V.IP()])
        [tiempo,intervalo] = self.getPingParameters()
        info("Starting Pings: %s ---> %s\n" % (str(C.IP()), str(V.IP())))
        p2 = C.popen(['ping', str(V.IP()),
                               '-i', str(intervalo),
                               '-c', str(tiempo)],
                              stdout=PIPE)
        for line in p2.stdout:
            # sys.stdout.write(line)
            logfile.write(line)
        p2.wait()

        logfile.close()
        p1.kill()
        info("*** End attack measure ***\n")

    def printOutputFile(self):
        info("***Output of ping: %s ---> %s ***\n\n"%(str(self.__hM.IP()),str(self.__hDst.IP())))
        lines = open(self.getFileName()).readlines()
        for l in lines:
            info("%s"%(l))
        info("\n")


def test1():
    info('*** Create the file config \n')
    medida = PingMeasure()

    "Create Simple topology example."
    net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
    # Initialize topology

    # Add containers
    h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
    h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
    h3 = net.addHost('h3', ip='10.0.0.3')  # Victima
    medida.configHosts(h2,h3)

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
    medida.medir()

    info('*** Stopping network')
    net.stop()
    medida.printOutputFile()
    medida.formatFile()


def test2():
    info('*** Create the file config \n')
    medida = PingMeasureAttack()

    "Create Simple topology example."
    net = Mininet(switch=OVSSwitch, build=False, link=TCLink)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)
    # Initialize topology

    # Add containers
    h1 = net.addHost('h1', ip='10.0.0.1')  # Cliente
    h2 = net.addHost('h2', ip='10.0.0.2')  # Atacante
    h3 = net.addHost('h3', ip='10.0.0.3')  # Victima
    medida.configAttack(h2,h3,h1,'u500')


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
    medida.medirAtaque()

    info('*** Stopping network')
    net.stop()
    medida.printOutputFile()
    medida.formatFile()



if __name__ == "__main__":
    setLogLevel('info')
    #test1()
    test2()