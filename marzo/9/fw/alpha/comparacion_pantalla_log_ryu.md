# Comparacion salida en pantalla en mininet y salida del archivo tras la ejecucion de ping#

## Trafico normal ##

### Unidad experimental ###

```python
ue1 = UnidadExperimental(topo=SingleSwitchTopo(k = 3, bw = 100),controller=RYU('c0'))
ue1.definirNodosClaves('h1','h2','h3')
```

### Salidas ###

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

## Trafico ataque ##

### Unidad experimental ###

```python
ue1 = UnidadExperimental(topo=SingleSwitchTopo(k = 3, bw = 100),controller=RYU('c0'))
ue1.definirNodosClaves('h1','h2','h3')
```
### Salidas ###

#### Consola mininet ####

```bash
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
(h1, s1) (h2, s1) (h3, s1) 
*** Configuring hosts
h1 h2 h3 
Configurando clase asociada al trafico
*** Starting controller
c0 
*** Starting 1 switches
s1 ...
*** Ping: testing ping reachability
h1 -> X h3 
h2 -> h1 h3 
h3 -> h1 h2 
*** Results: 16% dropped (5/6 received)
Starting Pings: 10.0.0.2 ---> 10.0.0.3
*** h2 : ('ping -c', 10, '-i', 1.0, '10.0.0.3')
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.021 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.074 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.135 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.064 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.046 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.077 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.170 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.067 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.060 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.080 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9194ms
rtt min/avg/max/mdev = 0.021/0.079/0.170/0.041 ms
End pings ***
Starting Pings: 10.0.0.2 ---> 10.0.0.3
Open file: ping_ataque_ryu.log
End pings ***
*** Starting CLI:
containernet> 
```

#### Archivo de texto ####

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.065 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.070 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.080 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.064 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.073 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.076 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.045 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9207ms
rtt min/avg/max/mdev = 0.045/0.072/0.083/0.012 ms
```

**Conclusion**:
1. Los resultados son muy parecidos incluso a los del caso normal. ¿Se estara lanzando el ataque?
2. No esta mostrandose la salida ```End attack``` en el bash. Propia del siguiente fragmento de código:

    ```python
    ...
    process_attack.kill()
    info("End attack ***\n")
    ```