# Informe #


## Ejecucion ##

**Controlador**

```bash
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
```

**Test Mininet**

```bash
sudo python topo-test.py
```


## Archivos resultantes ##

**ping.out**

```
PING 10.0.0.252 (10.0.0.252) 56(84) bytes of data.
64 bytes from 10.0.0.252: icmp_seq=1 ttl=64 time=3.78 ms
64 bytes from 10.0.0.252: icmp_seq=2 ttl=64 time=0.179 ms
64 bytes from 10.0.0.252: icmp_seq=3 ttl=64 time=0.052 ms
64 bytes from 10.0.0.252: icmp_seq=4 ttl=64 time=0.054 ms
64 bytes from 10.0.0.252: icmp_seq=5 ttl=64 time=0.052 ms
```


**iperf.out**
```
------------------------------------------------------------
Client connecting to 10.0.0.252, TCP port 5001
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[  3] local 10.0.0.251 port 39196 connected with 10.0.0.252 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 2.0 sec   229 MBytes   961 Mbits/sec
[  3]  2.0- 4.0 sec   228 MBytes   956 Mbits/sec
[  3]  4.0- 6.0 sec   227 MBytes   952 Mbits/sec
[  3]  6.0- 8.0 sec   226 MBytes   948 Mbits/sec
[  3]  8.0-10.0 sec   228 MBytes   957 Mbits/sec
[  3]  0.0-10.0 sec  1.11 GBytes   953 Mbits/sec
```

Tambien salen los archivos **iperf.err** y **ping.err** sin embargo hasta el momento estos dan vacios.


## Temas de discucion ##


### Sobre el ping ###

El ping cuando se ejecuta en consola da el siguiente resultado:

```bash
ping -c 4 10.0.0.2

PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=3.30 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.276 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.035 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.045 ms

--- 10.0.0.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3051ms
rtt min/avg/max/mdev = 0.035/0.914/3.302/1.382 ms
```

### Sobre el iperf ###

Por lo menos la salida para este caso si es igual

```bash
iperf -t 10 -i 2 -c 10.0.0.2

------------------------------------------------------------
Client connecting to 10.0.0.2, TCP port 5001
TCP window size: 16.0 MByte (default)
------------------------------------------------------------
[ 14] local 10.0.0.1 port 47998 connected with 10.0.0.2 port 5001
[ ID] Interval       Transfer     Bandwidth
[ 14]  0.0- 2.0 sec  6.74 GBytes  28.9 Gbits/sec
[ 14]  2.0- 4.0 sec  6.62 GBytes  28.4 Gbits/sec
[ 14]  4.0- 6.0 sec  6.74 GBytes  29.0 Gbits/sec
[ 14]  6.0- 8.0 sec  6.79 GBytes  29.2 Gbits/sec
[ 14]  8.0-10.0 sec  6.85 GBytes  29.4 Gbits/sec
[ 14]  0.0-10.0 sec  33.7 GBytes  29.0 Gbits/sec

```

Vemos que las estadisticas aparecen, sin embargo en el caso del almacenamiento del archivo no.

## Pendientes ##

1. Ver con 100 segundos lo que se tiene hasta el momento.
