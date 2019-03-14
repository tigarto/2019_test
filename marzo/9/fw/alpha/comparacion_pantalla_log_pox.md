# Comparacion salida en pantalla en mininet y salida del archivo tras la ejecucion de ping#

## Trafico normal ##

### Unidad experimental ###

```python
ue2 = UnidadExperimental(topo=SingleSwitchTopo(k = 3, bw = 100),controller=POX('c0'))
ue2.definirNodosClaves('h1','h2','h3')
```

### Saludas ###

#### Consola mininet ####

```bash
Starting Pings: 10.0.0.2 ---> 10.0.0.3
*** h2 : ('ping -c', 10, '-i', 1.0, '10.0.0.3')
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.134 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.097 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.066 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.079 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.081 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.069 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.072 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.086 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=32.7 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.081 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9187ms
rtt min/avg/max/mdev = 0.066/3.354/32.781/9.809 ms
```

#### Archivo de texto ####

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.057 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.081 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.048 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.073 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.076 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.039 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.081 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.106 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.100 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.082 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9198ms
rtt min/avg/max/mdev = 0.039/0.074/0.106/0.021 ms
```

**Conclusiones**:
1. Los valores son muy distintos; sin embargo,  el tiempo en el archivo de POX es cercano al del RYU asi que vamos a confiar que todo esta bien.
   
