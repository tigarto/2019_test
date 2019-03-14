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
   
## Trafico ataque ##

### Unidad experimental ###

```python
ue2 = UnidadExperimental(topo=SingleSwitchTopo(k = 3, bw = 100),controller=POX('c0'))
ue2.definirNodosClaves('h1','h2','h3')
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
h1 -> h2 h3 
h2 -> h1 h3 
h3 -> h1 h2 
*** Results: 0% dropped (6/6 received)
Launch attack: 10.0.0.1 ---> 10.0.0.3
Starting pings ***
*** h2 : ('ping -c', 10, '-i', 1.0, '10.0.0.3')
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.182 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.037 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.040 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.048 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.044 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.039 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.037 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.037 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.037 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 9 received, 10% packet loss, time 9218ms
rtt min/avg/max/mdev = 0.037/0.055/0.182/0.045 ms
End pings ***
End attack ***
Launch attack: 10.0.0.1 ---> 10.0.0.3
Starting pings ***
End pings ***
End attack ***
*** Starting CLI:
containernet> 
```

#### Archivo de texto ####

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 0 received, 100% packet loss, time 9203ms
```

**Conclusion**:
1. Si se ve el efecto del ataque en este controlador, sobre todo cuando se analiza el archivo de texto:
   
   **Salida en consola**

   * **Caso normal**: 
   
    ```
    --- 10.0.0.3 ping statistics ---
    10 packets transmitted, 10 received, 0% packet loss, time 9187ms
    rtt min/avg/max/mdev = 0.066/3.354/32.781/9.809 ms
    ```

   * **Caso ataque**: 
  
    ```
    --- 10.0.0.3 ping statistics ---
    10 packets transmitted, 9 received, 10% packet loss, time 9218ms
    rtt min/avg/max/mdev = 0.037/0.055/0.182/0.045 ms
    ```

    **Salida en archivo**

    * **Caso normal**: 
   
    ```
    --- 10.0.0.3 ping statistics ---
    10 packets transmitted, 10 received, 0% packet loss, time 9198ms
    rtt min/avg/max/mdev = 0.039/0.074/0.106/0.021 ms
    ```

   * **Caso ataque**: 
  
    ```
    PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.

    --- 10.0.0.3 ping statistics ---
    10 packets transmitted, 0 received, 100% packet loss, time 9203ms
    ```


