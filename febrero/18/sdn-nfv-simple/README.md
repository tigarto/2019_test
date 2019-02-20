

El ejemplo se tomo de la siguiente pagina web: [Simple SDN/NFV example](http://csie.nqu.edu.tw/smallko/sdn/simple_nfv_sdn.htm) cuya descripción en palabras del autor es la siguiente:


> Network function virtualization (NFV) is a network architecture concept that uses the technologies of IT virtualization to virtualize entire classes of network node functions into building blocks that may connect, or chain together, to create communication services. SDN can be handling the routing.


**A simple example**

```
H1---S1---H2
     |
     |
     H3
```
 

In this example, H1 will send "Hello, World!" to H2. If the link between S1 and H2 is lossy. The message may be lost duration transmission. If we can add the NFV at the node 3 and route the packet from H1 to H3 first, duplicate the packets and send back to H2, the message has a higher probability of reaching H2. (Note that we don’t modify the source code of sender program.)


1. **Case 1**: H1 is sending traffic to H2 directly.

* Iniciar la red: 
```bash
# Terminal del bash
sudo mn --topo single,3 --mac --controller=remote
```

* Agregar las reglas:
  
```bash
# Terminal de mininet
sh ovs-ofctl add-flow s1 priority=1,in_port=1,actions=output:flood
sh ovs-ofctl add-flow s1 priority=1,in_port=2,actions=output:flood
sh ovs-ofctl add-flow s1 priority=1,in_port=3,actions=output:flood
sh ovs-ofctl add-flow s1 priority=10,ETH_TYPE = 0x0800,nw_dst=10.0.0.1,actions=output:1
sh ovs-ofctl add-flow s1 priority=10,ETH_TYPE = 0x0800,nw_dst=10.0.0.2,actions=output:2
sh ovs-ofctl add-flow s1 priority=10,ETH_TYPE = 0x0800,nw_dst=10.0.0.3,actions=output:3
```

* Iniciar las aplicaciones tanto en H1 como en H2

Lanzanddo las terminales de los hosts:

```bash
# Terminal mininet
xterm h1 h2
```



```bash
# Terminal h2
python 
python udp_receive.py 

```

```bash
# Terminal h1
python python udp_send.py 

```

Las salidas dieron tal y como se esperaba.

2. **Case 2**: set the rules so that the packet sent by H1 can be routed to H3 first. Then H3 will duplicate the received packets and send back to H2.

With the following rules, H1 send one packet and H2 can receive two packets. (No need to do anything at the sender side and receiver side.)

```bash
# Terminal de mininet
# Se agrego esta regla
sh ovs-ofctl add-flow s1 priority=100,in_port=1,actions=mod_dl_dst:00:00:00:00:00:03,mod_nw_dst:10.0.0.3,output:3
```

 

```bash
sh ovs-ofctl add-flow s1 priority=100,in_port=1,actions=mod_dl_dst:00:00:00:00:00:03,mod_nw_dst:10.0.0.3,output:3
```

## Referencias ##

1. https://github.com/intracom-telecom-sdn
2. https://github.com/intracom-telecom-sdn/oftraf
