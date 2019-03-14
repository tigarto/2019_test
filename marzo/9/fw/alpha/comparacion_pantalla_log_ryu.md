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
h1 -> h2 h3 
h2 -> h1 h3 
h3 -> h1 h2 
*** Results: 0% dropped (6/6 received)
Launch attack: 10.0.0.1 ---> 10.0.0.3
Starting pings ***
*** h2 : ('ping -c', 10, '-i', 1.0, '10.0.0.3')
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.041 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.030 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.021 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.021 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.023 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.022 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.022 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.021 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.020 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.029 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9222ms
rtt min/avg/max/mdev = 0.020/0.025/0.041/0.006 ms
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
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.038 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.016 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.023 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.019 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.019 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.022 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.026 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.020 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.027 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.023 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9210ms
rtt min/avg/max/mdev = 0.016/0.023/0.038/0.006 ms
```

**Conclusion**:
1. La comparación entre el caso normal y el con ataque si tiene sentido para la salida:
   
   **Salida en consola**

   * **Caso normal**: 
   
    ```
    --- 10.0.0.3 ping statistics ---
    10 packets transmitted, 10 received, 0% packet loss, time 9208ms
    rtt min/avg/max/mdev = 0.041/0.073/0.106/0.019 ms
    ```

   * **Caso ataque**: 
  
    ```
    --- 10.0.0.3 ping statistics ---
    10 packets transmitted, 10 received, 0% packet loss, time 9210ms
    rtt min/avg/max/mdev = 0.016/0.023/0.038/0.006 ms
    ```

    **Salida en archivo**

    * **Caso normal**: 
   
    ```
    --- 10.0.0.3 ping statistics ---
    10 packets transmitted, 10 received, 0% packet loss, time 9208ms
    rtt min/avg/max/mdev = 0.041/0.073/0.106/0.019 ms
    ```

   * **Caso ataque**: 
  
    ```
    --- 10.0.0.3 ping statistics ---
    10 packets transmitted, 10 received, 0% packet loss, time 9210ms
    rtt min/avg/max/mdev = 0.016/0.023/0.038/0.006 ms
    ```

2. Los resultados son muy parecidos incluso a los del caso normal. ¿Se estara lanzando el ataque?
