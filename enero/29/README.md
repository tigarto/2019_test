# Ensayos #



## Algunos aspectos a tener en cuenta ##

Tomado de: https://github.com/mininet/mininet/wiki/Introduction-to-Mininet 

```
These are recommended, though you’re free to use any tool you’re familiar with.

1. Bandwidth (bwm-ng, ethstats)
2. Latency (use ping)
3. Queues (use tc included in monitor.py)
4. TCP CWND statistics (tcp_probe, maybe we should add it to monitor.py)
5. CPU usage (global: top, or per-container cpuacct)
```

Se instalaron las herramientas bwm-ng y ethstats.

Por lo menos la parte de los retardos se elige con el avg del ping.

### Metricas que uno ve ###

**Algunos enlaces de consulta**:
* Herramienta de ataque: [hping3](https://www.blackmoreops.com/2015/04/21/denial-of-service-attack-dos-using-hping3-with-spoofed-ip-in-kali-linux/) 
* https://es.slideshare.net/Himani-Singh/type-of-ddos-attacks-with-hping3-example
* https://pentest.blog/how-to-perform-ddos-test-as-a-pentester/
* https://www.pedrocarrasco.org/manual-practico-de-hping/

1. **Articulo 1**: A Port Hopping Based DoS Mitigation Scheme in SDN Network


**Experimento**

* Mininet simulator
* OVS switches
* NOX SDN controller
* the client, the server and the attackers (single node can run multiple attack codes)

**Metricas**

**Metrica 1**: Packet length (KB) .vs. CPU load (%)

1. Para obtener el CPU load:

Obtener PID:

```bash
ps -aux | grep ryu-manager
```

Luego obtener el consumo de CPU:

```bash
htop -p  PID
top -n -p PID
```

Hasta el momento veo mejor htop. No logro interpretar top como quisiera.

2. Sobre el ataque: La idea es "construct a typical SYN (synchronize) flood DoS attack tool using hping3 and carry out DoS attack to
available ports of the protected server one by one". El 

```bash
hping3 -V -S -d SIZE --flood ip_victima
```


**Metrica 2**: DoS attack rate (MB/s) .vs. Response time (ms)


La tasa de paquetes por segundo se fija con la opcion -i:

```bash
#Fijando la tasa
-i --interval
```

Donde **--interval** estara definido en X segundos o uX microsegundos. Por ejemplo:

```bash
#Tasa de envio de 10 paquetes por segundo
hping3 ... -i u10000 ...

#Tasa de envio de 1 paquete por segundo
hping3 ... -i 1 ...
```


**Time (s) .vs. Transmission success rate (%)**

Aun pendiente, no se como sacarlo


**Articulo 2**: A Feasible Method to combat against DDoS Attack in SDN Network


**Experimento**

* Opnet
* small topology which consists of 1 webserver and 03 PC clients (1 DDoS attacking user, 1 malicious user and 1 frequent user)
* switch: capacity of 10.000 entries. Initially, it is empty. The normal entry has hard timeout and idle timeout equal to 600 seconds and 60 seconds. The entry for DDoS attacking user has hard timeout and idle timeout equal to (60, 10) seconds.
* malicious user has IP address 10.0.0.1: It injects spoofed packets to the switch infinitely. For each packet, the destination IP address is generated randomly.
* The DDoS attacking user sends spoofed packets to the switch infinitely. For each packet, the source and destination IP addresses are generated randomly.
* The frequent user has IP address 10.0.0.2. It establishes 5 different connections to the server, and transmits 10 packets per connections.


**Metricas**

**Metrica 1**: time (sec) .vs. Number of entries in flow table (con y sin el metodo).

**Metrica 2**: time (sec) .vs. Number of packets arrive at the controller (con y sin el metodo).

**Metrica 3**: Time (sec) .vs. Bandwidth of the controller−switch channel (kbps)


**Articulo 3**: FloodDefender: Protecting Data and Control Plane Resources under SDN-aimed DoS Attacks



**Articulo 4**: The Effects of DoS Attacks on ODL and POX SDN Controllers

**Articulo 5**: Experimental Evaluation of the Impact of DoS Attacks in SDN

**Articulo 6**: Detection and Mitigation of Denial of Service (DoS) Attacks Using Performance Aware Software Defined Networking (SDN)

**Articulo 7**: DDOS Detection and Denial using Third Party Application in SDN

**Articulo 8**: SECOD: SDN sEcure COntrol and Data Plane Algorithm for Detecting and Defending against DoS Attacks

FloodShield: Securing the SDN Infrastructure Against Denial-of-Service Attacks

Towards A Secure SDN Architecture

https://www.kali.org/news/official-kali-linux-docker-images/
https://hub.docker.com/r/kalilinux/kali-linux-docker/


## Ensayos ##

### Ensayo 1 - Con Ryu ###


```bash
# Terminal ryu
ryu-manager --verbose simple_switch_13.py ofctl_rest.py
```

```bash
# Terminal mininet
sudo mn --topo single,3 --mac --controller remote --link tc,bw=10 --switch ovsk,protocols=OpenFlow13
```


```bash
# Terminal configuracion del switch
sudo ovs-vsctl set bridge s1 protocols=OpenFlow13
```

En el caso anterior se limito el ancho de banda del enlace a 10 Mbps. Luego en la terminal del host h1 se envio el ataque:


```bash
# Ataque
hping3 -V -c 1000000 --flood --rand-source 10.0.0.3
^C
```

Aqui la cosa si cambia:
1. Sin el ataque: 
   *  iperf h2 h3: ['9.57 Mbits/sec', '10.1 Mbits/sec']
   *  h1 ping -c 10 h2: rtt min/avg/max/mdev = 0.053/0.082/0.099/0.018 ms
2. Con el ataque:
   *  iperf h2 h3: ['295 Kbits/sec', '699 Kbits/sec']
   *  h1 ping -c 10 h2: rtt min/avg/max/mdev = 7.086/9.314/11.184/1.567 ms

### Ensayo 2 - Con Faucet ###

Arrancar el faucet.

```bash
# Arrancando el bash del contenedor faucet
sudo docker run -it \
    --name faucet \
    --restart=always \
    -v /etc/faucet/:/etc/faucet/ \
    -v /var/log/faucet/:/var/log/faucet/ \
    -p 6653:6653 \
    -p 9302:9302 \
    -p 8080:8080 \
    faucet/faucet \
    bash

# Ejecutando faucet con la aplicacion ofctl_rest para hacer consultas restful
cd /usr/lib/python3.6/site-packages/ryu/app 
faucet -v --ryu-app ofctl_rest.py
```

Arrancar el gauge.

```bash
# Arrancando el basf el contenedor gauge
sudo docker run -it \
    --name gauge \
    --restart=always \
    -v /etc/faucet/:/etc/faucet/ \
    -v /var/log/faucet/:/var/log/faucet/ \
    -p 6654:6653 \
    -p 9303:9303 \
    faucet/gauge \
    bash

# Ejecutando el gauge
gauge -v
```

3. Verificar en el prometheus que los targets este listos: http://localhost:9090/targets


Llevar a cabo el ataque desde la terminal h1:

```bash
# Ataque
hping3 -V -c 1000000 --flood --rand-source 10.0.0.253
^C
```

Aqui la cosa si cambia:
1. Sin el ataque: 
   *  iperf h2 h3: ['9.57 Mbits/sec', '10.0 Mbits/sec']
   *  h1 ping -c 10 h2: rtt min/avg/max/mdev = 0.043/0.067/0.106/0.019 ms

2. Con el ataque:
   *  iperf h2 h3: ['183 Kbits/sec', '236 Kbits/sec']
   *  h1 ping -c 10 h2: rtt min/avg/max/mdev = 43.168/43.195/43.224/0.228 ms


## Ensayo 3 ##

Descargando linear linearbandwidth.py: https://raw.githubusercontent.com/mininet/mininet/master/examples/

https://github.com/mininet/mininet/blob/master/examples/scratchnet.py
https://github.com/mininet/mininet/blob/master/examples/simpleperf.py

https://github.com/mininet/mininet/blob/master/examples/scratchnetuser.py


Veamos mas medidas:

https://github.com/mininet/mininet/wiki/Introduction-to-Mininet

http://cial.csie.ncku.edu.tw/presentation/group_pdf/Dynamic%20Traffic%20Diversion%20in%20SDN%20Testbed%20vs%20Mininet.pdf

https://stackoverflow.com/questions/43287437/compare-sdn-mininet-results-to-traditional-network-results/43312501

## Enlaces ##

### Sobre colas###

1. https://www.southampton.ac.uk/~drn1e09/ofertie/openflow_qos_mininet.pdf
2. http://csie.nqu.edu.tw/smallko/sdn/mySDN_Lab5.pdf

### Sobre hping3 ###

1. http://0daysecurity.com/articles/hping3_examples.html
2. https://www.redeszone.net/gnu-linux/hping3-manual-de-utilizacion-de-esta-herramienta-para-manipular-paquetes-tcp-ip/
3. https://tools.kali.org/information-gathering/hping3
4. Google: hping3 lab pdf
5. http://www.blog.xentech.cl/2016/01/07/denegacion-de-servicios-con-hping3-kali-linux/
6. https://f5-agility-labs-firewall.readthedocs.io/en/latest/class1/lab3/3a-02.html
7. http://lms.uop.edu.jo/lms/pluginfile.php/403/mod_resource/content/0/Lab-Hping3.pdf
8. https://www.binarytides.com/tcp-syn-flood-dos-attack-with-hping/
9. http://0daysecurity.com/articles/hping3_examples.html
10. https://n0where.net/dos-attack-with-hping3
11. https://www.rationallyparanoid.com/articles/hping.html
12. https://securityonline.info/syn-flood-attack-using-hping3/?cn-reloaded=1
13. https://lamiradadelreplicante.com/2012/01/24/ataque-ddos-syn-flood-con-hping3/
14. https://www.pedrocarrasco.org/manual-practico-de-hping/


### Estadisticas ###
1. https://github.com/topics/ethstats
2. https://github.com/mininet/mininet/blob/master/examples/cpu.py
3. https://pdfs.semanticscholar.org/afa6/c64530461075c886821bdebd067b997f6443.pdf
4. https://core.ac.uk/download/pdf/71398860.pdf
5. https://sourceforge.net/p/ryu/mailman/message/35639154/
6. https://rc.library.uta.edu/uta-ir/bitstream/handle/10106/26824/VERMA-THESIS-2017.pdf?sequence=1
7. https://www.udemy.com/learn-sdn-with-mininet-ryu-exercises/
8. https://github.com/knetsolutions/learn-sdn-with-ryu
9. https://mailman.stanford.edu/pipermail/mininet-discuss/2015-October/006519.html 
10. https://www.uni-bamberg.de/fileadmin/uni/fakultaeten/wiai_lehrstuehle/informatik_ktr/Dateien/Publikationen/AutoMininet.pdf
11. https://github.com/mininet/mininet/blob/master/examples/linearbandwidth.py


### Otros ###

1. http://mininet.org/walkthrough/
2. https://www.telematika.org/snippet/008-mininet/
3. http://extraconversion.com/es/almacenamiento-de-datos/bytes/bytes-a-bits.html
4. http://www.iv2-technologies.com/DOSAttacks.pdf


hping3 -V -c 1000 --flood --rand-source 10.0.0.3


