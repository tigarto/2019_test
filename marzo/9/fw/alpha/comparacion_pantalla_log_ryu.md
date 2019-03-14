# Comparacion salida en pantalla en mininet y salida del archivo tras la ejecucion de ping#

## Trafico normal ##

### Unidad experimental ###

```python
ue1 = UnidadExperimental(topo=SingleSwitchTopo(k = 3, bw = 100),controller=RYU('c0'))
ue1.definirNodosClaves('h1','h2','h3')
```

### Saludas ###

#### Consola mininet ####

```bash
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.041 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.087 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.087 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.059 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.058 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.057 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.070 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.081 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.106 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.086 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9208ms
rtt min/avg/max/mdev = 0.041/0.073/0.106/0.019 ms
```

#### Archivo de texto ####

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.041 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.087 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.087 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.059 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.058 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.057 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.070 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.081 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.106 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.086 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9208ms
rtt min/avg/max/mdev = 0.041/0.073/0.106/0.019 ms
```

**Conclusiones**:
1. Los valores son muy proximos.