# Descripción esperimental #

## Sobre el experimento ##


### Herramientas empleadas ###

* **Hardware**:
    * Lenovo Z50 con ubuntu 16.04 LTS, con un procesador Intel Core i7 ...
* **Sofware empleado**:
    * [**Mininet**](http://mininet.org/overview/): emulador para la generación y desarrollo de pruebas en topologias de red en un PC.
    * **ping**: para la medición del RTT y packet delivery ratio.
    * **iperf**: para la medición del ancho de banda.
    * **hping3**: herramienta empleada para la generación de trafico de ataque.
    * **switch**: Openswitch
    * **Controladores**: Ryu y Faucet
  
### Topologia ###

A continuacion se muestra la topologia de test en su caso mas simple:

![topologia-test](topologia-test.png)

La siguiente tabla describe el papel de los host en el experimento:

| Host | Descripción | IP |
|------|-------------|-------------|
| h1   | Atacante    | 10.0.0.1    |
| h2   | Cliente    | 10.0.0.2    |
| h3   | Victima    | 10.0.0.3    |

En lo que respecta al switch y al controlador, se empleara OpenvSwitch y Ryu respectivamente. Las aplicaciones que se ejecutará en el controlador serán el [simple_switch_13.py](simple_switch_13.py) (para manejo de paquetes) y [ofctl_rest.py](ofctl_rest.py) (para obtención de estadisticas usando REST). Una vez clarificado el procedimiento de experimentación con Ryu se procederá a replicar las pruebas con Faucet.

### Protocolo de prueba manual ###

En este caso las pruebas se harian de modo manual empleando el cli de mininet. El protocolo seria el siguiente:
1. Iniciar el controlador:

```bash
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
```
2. Iniciar la topologia:

```bash
sudo mn --topo=single,3 --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1:6653  --link=tc,bw=100 
```

3. Realizar las pruebas en mininet una vez este se cargue:

```bash
containernet>
```

Algunos comandos utilizados simples:
1. **```pingall```**:

```bash
containernet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 
h2 -> h1 h3 
h3 -> h1 h2 
*** Results: 0% dropped (6/6 received)
```

2. **```h1 ping -c 10 -i 0.5 h2```** para hacer pruebas simples:

```bash
containernet>  h1 ping -c 10 -i 0.5 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.317 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.093 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.109 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.092 ms
64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=0.096 ms
64 bytes from 10.0.0.2: icmp_seq=6 ttl=64 time=0.102 ms
64 bytes from 10.0.0.2: icmp_seq=7 ttl=64 time=0.093 ms
64 bytes from 10.0.0.2: icmp_seq=8 ttl=64 time=0.099 ms
64 bytes from 10.0.0.2: icmp_seq=9 ttl=64 time=0.092 ms
64 bytes from 10.0.0.2: icmp_seq=10 ttl=64 time=0.041 ms

--- 10.0.0.2 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 4627ms
rtt min/avg/max/mdev = 0.041/0.113/0.317/0.070 ms
```

De las mediciones 1 y 2 se pueden obtener metricas como el Packet delivery ratio y el RTT asociado al delay.

3. **```iperf```**:

```bash
containernet> iperf
*** Iperf: testing TCP bandwidth between h1 and h3 
*** Results: ['95.7 Mbits/sec', '96.8 Mbits/sec']
```

4. **```iperf h2 h3```**:
   
```bash
containernet> iperf h2 h3
*** Iperf: testing TCP bandwidth between h2 and h3 
*** Results: ['95.7 Mbits/sec', '96.8 Mbits/sec']
```

5. Uso de iperf empleando h2 como cliente iperf y h3 como servidor iperf (se acceden a cada una de las consolas con iperf **```xterm h2 h3```**):

    1. Arrancar el servidor iperf: 
   
        ```bash
        # Consola h3
        root@fuck-pc:~/Documents/tesis_2019-1/tests/febrero/04# iperf -s
        ------------------------------------------------------------
        Server listening on TCP port 5001
        TCP window size: 85.3 KByte (default)
        ------------------------------------------------------------

        ```

    2. Arrancar el cliente iperf:

        ```bash
        # Consola h2
        root@fuck-pc:~/Documents/tesis_2019-1/tests/febero/04# iperf -t 10 -i 1 -c 10.0.0.3
        ------------------------------------------------------------
        Client connecting to 10.0.0.3, TCP port 5001
        TCP window size: 85.3 KByte (default)
        ------------------------------------------------------------
        [ 16] local 10.0.0.2 port 36062 connected with 10.0.0.3 port 5001
        [ ID] Interval       Transfer     Bandwidth
        [ 16]  0.0- 1.0 sec  12.2 MBytes   103 Mbits/sec
        [ 16]  1.0- 2.0 sec  11.1 MBytes  93.3 Mbits/sec
        [ 16]  2.0- 3.0 sec  11.5 MBytes  96.5 Mbits/sec
        [ 16]  3.0- 4.0 sec  11.5 MBytes  96.5 Mbits/sec
        [ 16]  4.0- 5.0 sec  11.2 MBytes  94.4 Mbits/sec
        [ 16]  5.0- 6.0 sec  11.5 MBytes  96.5 Mbits/sec
        [ 16]  6.0- 7.0 sec  11.5 MBytes  96.5 Mbits/sec
        [ 16]  7.0- 8.0 sec  11.5 MBytes  96.5 Mbits/sec
        [ 16]  8.0- 9.0 sec  11.2 MBytes  94.4 Mbits/sec
        [ 16]  9.0-10.0 sec  11.5 MBytes  96.5 Mbits/sec
        [ 16]  0.0-10.0 sec   115 MBytes  96.3 Mbits/sec
        root@fuck-pc:~/Documents/tesis_2019-1/tests/febrero/04# 
        ```

De las mediciones asociadas con el iperf se pueden obtener el ancho de banda asociado con el link.







### Metricas llevadas a cabo ###



### ###

## Referencias ##

1. [Cyberpaths - Network Traffic & Denial of Service Lab](http://mountrouidoux.people.cofc.edu/CyberPaths/networktrafficandddos.html)
2. [OpenState-SDN/ryu](https://github.com/OpenState-SDN/ryu/wiki/DDoS)
3. [DDoS Attack Detection in SDN-based VANET Architectures](https://projekter.aau.dk/projekter/files/239545035/Master_Thesis___DDoS_Attack_Detection_in_SDN_based_VANET_Architectures__group_1097.pdf)
4. [CS244 ’13: LOW RATE TCP-TARGETED DOS ATTACK](https://reproducingnetworkresearch.wordpress.com/2013/03/13/cs-244-13-low-rate-tcp-targeted-dos-attack/)
5. [CS244 ’17: LOW-RATE TCP DOS ATTACKS](https://reproducingnetworkresearch.wordpress.com/2017/06/05/cs244-17-low-rate-tcp-dos-attacks/)
6. [Hping3](https://github.com/jkotrady/hping/wiki/Hping3)
7. [Hping3 Packet Grenade](https://gist.github.com/Erreinion/c810b9561ffa423cca01)
8. [detecting Dos attacks on mininet](https://seclists.org/snort/2016/q3/83)
9. [OpenState-SDN/ryu](https://github.com/OpenState-SDN/ryu/wiki/DDoS)
10. A Software Approach for Mitigation of DoS Attacks on SDN’s (Software-Defined Networks)
    1.  [Enlace 1](https://books.google.com.co/books?id=nHhqDwAAQBAJ&pg=PA338&lpg=PA338&dq=hping+dos+mininet&source=bl&ots=Et2tD5_m38&sig=ACfU3U2FcCLvdcgzplni51qgiqOeOMJd7g&hl=es&sa=X&ved=2ahUKEwiOyoLN26LgAhVyrlkKHT6-D1k4ChDoATACegQIBxAB#v=onepage&q=hping%20dos%20mininet&f=false)
    2.  [Enlace 2](https://github.com/mishra14/DDoSAttackMitigationSystem)
11. [kawaljeet024/DDOS-Attack-using-Entropy-method-in-SDN-environmnet](https://github.com/kawaljeet024/DDOS-Attack-using-Entropy-method-in-SDN-environmnet)
12. [wenjoseph/TCPDoS](https://github.com/wenjoseph/TCPDoS)
13. [krishnatejay/research  ](https://github.com/krishnatejay/research)
14. [rprabhuh/SDNDDoS](https://github.com/rprabhuh/SDNDDoS)
15. [Automatic Detection of Elephant flows through Openflow-based OpenvSwitch](http://trap.ncirl.ie/2873/1/spurthimallesh.pdf)
16. [pblanc5/Mininet-Simulated-DDOS](https://github.com/pblanc5/Mininet-Simulated-DDOS)
17. [omkarsuram/SDN-DDoS](https://github.com/omkarsuram/SDN-DDoS)












