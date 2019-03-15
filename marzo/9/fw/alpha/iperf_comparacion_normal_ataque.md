# Comparación entre iperf normal y de ataque #

Solo se emplearan los archivos de salida:

## Normal ##

**RYU**

```
------------------------------------------------------------
Client connecting to 10.0.0.3, TCP port 5001
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[  3] local 10.0.0.2 port 51712 connected with 10.0.0.3 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec  12.1 MBytes   102 Mbits/sec
[  3]  1.0- 2.0 sec  11.4 MBytes  95.4 Mbits/sec
[  3]  2.0- 3.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  3.0- 4.0 sec  11.4 MBytes  95.4 Mbits/sec
[  3]  4.0- 5.0 sec  11.2 MBytes  94.4 Mbits/sec
[  3]  5.0- 6.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  6.0- 7.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  7.0- 8.0 sec  11.2 MBytes  94.4 Mbits/sec
[  3]  8.0- 9.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  9.0-10.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  0.0-10.0 sec   115 MBytes  96.2 Mbits/sec
```

**POX**

```
------------------------------------------------------------
Client connecting to 10.0.0.3, TCP port 5001
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[  3] local 10.0.0.2 port 51824 connected with 10.0.0.3 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec  12.1 MBytes   102 Mbits/sec
[  3]  1.0- 2.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  2.0- 3.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  3.0- 4.0 sec  11.1 MBytes  93.3 Mbits/sec
[  3]  4.0- 5.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  5.0- 6.0 sec  11.8 MBytes  98.6 Mbits/sec
[  3]  6.0- 7.0 sec  11.1 MBytes  93.3 Mbits/sec
[  3]  7.0- 8.0 sec  11.6 MBytes  97.5 Mbits/sec
[  3]  8.0- 9.0 sec   640 KBytes  5.24 Mbits/sec
[  3]  9.0-10.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 10.0-11.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 11.0-12.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 12.0-13.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 13.0-14.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 14.0-15.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 15.0-16.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 16.0-17.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 17.0-18.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 18.0-19.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 19.0-20.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 20.0-21.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 21.0-22.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 22.0-23.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 23.0-24.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 24.0-25.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 25.0-26.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 26.0-27.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 27.0-28.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 28.0-29.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 29.0-30.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 30.0-31.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 31.0-32.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 32.0-33.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 33.0-34.0 sec  0.00 Bytes  0.00 bits/sec
[  3] 34.0-35.0 sec  0.00 Bytes  0.00 bits/sec
[  3]  0.0-35.2 sec  93.0 MBytes  22.1 Mbits/sec
```

Sin embargo:
```
containernet> iperf
*** Iperf: testing TCP bandwidth between h1 and h3 
*** Results: ['95.6 Mbits/sec', '96.8 Mbits/sec']
```

Pero en otra prueba:

```
------------------------------------------------------------
Client connecting to 10.0.0.3, TCP port 5001
TCP window size: 93.5 KByte (default)
------------------------------------------------------------
[  3] local 10.0.0.2 port 51976 connected with 10.0.0.3 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec  12.0 MBytes   101 Mbits/sec
[  3]  1.0- 2.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  2.0- 3.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  3.0- 4.0 sec  11.2 MBytes  94.4 Mbits/sec
[  3]  4.0- 5.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  5.0- 6.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  6.0- 7.0 sec  11.1 MBytes  93.3 Mbits/sec
[  3]  7.0- 8.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  8.0- 9.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  9.0-10.0 sec  11.2 MBytes  94.4 Mbits/sec
[  3]  0.0-10.0 sec   115 MBytes  96.2 Mbits/sec
```

Y  en otra:

```
------------------------------------------------------------
Client connecting to 10.0.0.3, TCP port 5001
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[  3] local 10.0.0.2 port 52078 connected with 10.0.0.3 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec  12.1 MBytes   102 Mbits/sec
[  3]  1.0- 2.0 sec  11.4 MBytes  95.4 Mbits/sec
[  3]  2.0- 3.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  3.0- 4.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  4.0- 5.0 sec  11.1 MBytes  93.3 Mbits/sec
[  3]  5.0- 6.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  6.0- 7.0 sec  11.6 MBytes  97.5 Mbits/sec
[  3]  7.0- 8.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  8.0- 9.0 sec  11.2 MBytes  94.4 Mbits/sec
[  3]  9.0-10.0 sec  11.5 MBytes  96.5 Mbits/sec
[  3]  0.0-10.0 sec   115 MBytes  96.3 Mbits/sec
```

## Ataque ##

**RYU**

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.065 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.025 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.031 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.032 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.028 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.020 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.023 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.024 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.028 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.022 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9214ms
rtt min/avg/max/mdev = 0.020/0.029/0.065/0.014 ms

```

**POX**

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.159 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.044 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.041 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.042 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.037 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.084 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.039 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.037 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 8 received, 20% packet loss, time 9206ms
rtt min/avg/max/mdev = 0.037/0.060/0.159/0.040 ms
```

**Obsercaciones**:
1. Los codigos anteriores mostraban algo cuando no se bloqueaban. Sobre todo en el POX, pero el problema con los bloqueos hay que trabajarlos.

**Caso POX**

```python
# Fragmento de codigo (code snipped) de test
setLogLevel("info")

def killAlarma(p1,p2,p3):
        info("Hola alarma\n")
        os.kill(p1.pid, signal.SIGTERM)
        os.kill(p2.pid, signal.SIGTERM)
        os.kill(p3.pid, signal.SIGTERM)
        info("Chao alarma\n")   
        

ue = UnidadExperimental(topo=TopologiaTest(100),controller=RYU('c0'))
ue.definirNodosClaves('h1','h2','h3')


info("Configurando unidad experimental\n")
info("Configurando trafico normal\n")
info("Configurando la red\n")
net = Mininet(topo = ue.getTopo(), controller=ue.getController(), link=TCLink ,build=False)
net.build()
info("Configurando clase asociada al trafico\n")    
[A,C,V] = ue.obtenerNodosClaves()
A = net.get(A)
C = net.get(C)
V = net.get(V)
net.start()
net.pingAll()
log = open('salida_pox.log',"w")
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
            timer = threading.Timer(t + 2, killAlarma, 
                                    args=[atack_process,client_process,server_process])
            timer.start()
            timer.join()
            log.close()
            CLI(net)
            net.stop()    
```

Salida:

```bash
# Comando python
sudo python trafico.py 
# Salida mininet
Configurando unidad experimental
Configurando trafico normal
Configurando la red
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 h3 
*** Adding switches:
s1 
*** Adding links:
(100.00Mbit) (100.00Mbit) (100.00Mbit) (h1, s1) (100.00Mbit) (100.00Mbit) (100.00Mbit) (h2, s1) (100.00Mbit) (100.00Mbit) (100.00Mbit) (h3, s1) 
*** Configuring hosts
h1 h2 h3 
Configurando clase asociada al trafico
*** Starting controller
c0 
*** Starting 1 switches
s1 (100.00Mbit) (100.00Mbit) (100.00Mbit) ...(100.00Mbit) (100.00Mbit) (100.00Mbit) 
*** Ping: testing ping reachability
h1 -> h2 h3 
h2 -> h1 h3 
h3 -> h1 h2 
*** Results: 0% dropped (6/6 received)
*** Iniciando el servidor iperf ***
*** Lanzando el ataque ***
*** Lanzando el cliente iperf ***
Hola alarma
Chao alarma
*** Starting CLI:
containernet> sh cat salida_pox.log
```


**RYU**


```python
# Fragmento de codigo (code snipped) de test
setLogLevel("info")

def killAlarma(p1,p2,p3):
        info("Hola alarma\n")
        os.kill(p1.pid, signal.SIGTERM)
        os.kill(p2.pid, signal.SIGTERM)
        os.kill(p3.pid, signal.SIGTERM)
        info("Chao alarma\n")   
        

ue = UnidadExperimental(topo=TopologiaTest(100),controller=POX('c0'))
ue.definirNodosClaves('h1','h2','h3')


info("Configurando unidad experimental\n")
info("Configurando trafico normal\n")
info("Configurando la red\n")
net = Mininet(topo = ue.getTopo(), controller=ue.getController(), link=TCLink ,build=False)
net.build()
info("Configurando clase asociada al trafico\n")    
[A,C,V] = ue.obtenerNodosClaves()
A = net.get(A)
C = net.get(C)
V = net.get(V)
net.start()
net.pingAll()
log = open('salida_ryu.log',"w")
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
            timer = threading.Timer(t + 2, killAlarma, 
                                    args=[atack_process,client_process,server_process])
            timer.start()
            timer.join()
            log.close()
            CLI(net)
            net.stop()    
```

Salida:

```bash
# Comando python
sudo python trafico.py
# Consola mininet 
Configurando unidad experimental
Configurando trafico normal
Configurando la red
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 h3 
*** Adding switches:
s1 
*** Adding links:
(100.00Mbit) (100.00Mbit) (100.00Mbit) (h1, s1) (100.00Mbit) (100.00Mbit) (100.00Mbit) (h2, s1) (100.00Mbit) (100.00Mbit) (100.00Mbit) (h3, s1) 
*** Configuring hosts
h1 h2 h3 
Configurando clase asociada al trafico
*** Starting controller
c0 
*** Starting 1 switches
s1 (100.00Mbit) (100.00Mbit) (100.00Mbit) ...(100.00Mbit) (100.00Mbit) (100.00Mbit) 
*** Ping: testing ping reachability
h1 -> X h3 
h2 -> h1 h3 
h3 -> h1 h2 
*** Results: 16% dropped (5/6 received)
*** Iniciando el servidor iperf ***
*** Lanzando el ataque ***
*** Lanzando el cliente iperf ***
Hola alarma
Chao alarma
*** Starting CLI:
containernet> sh cat salida_ryu.log
------------------------------------------------------------
Client connecting to 10.0.0.3, TCP port 5001
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[ 21] local 10.0.0.2 port 45736 connected with 10.0.0.3 port 5001
[ ID] Interval       Transfer     Bandwidth
[ 21]  0.0- 1.0 sec  10.4 MBytes  87.0 Mbits/sec
[ 21]  1.0- 2.0 sec  8.88 MBytes  74.4 Mbits/sec
[ 21]  2.0- 3.0 sec  9.00 MBytes  75.5 Mbits/sec
[ 21]  3.0- 4.0 sec  9.50 MBytes  79.7 Mbits/sec
[ 21]  4.0- 5.0 sec  9.00 MBytes  75.5 Mbits/sec
[ 21]  5.0- 6.0 sec  9.38 MBytes  78.6 Mbits/sec
[ 21]  6.0- 7.0 sec  9.50 MBytes  79.7 Mbits/sec
[ 21]  7.0- 8.0 sec  9.00 MBytes  75.5 Mbits/sec
[ 21]  8.0- 9.0 sec  9.00 MBytes  75.5 Mbits/sec
[ 21]  9.0-10.0 sec  9.50 MBytes  79.7 Mbits/sec
[ 21]  0.0-10.0 sec  93.2 MBytes  78.0 Mbits/sec
containernet> 
```

