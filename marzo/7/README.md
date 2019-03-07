


Uso de sflow tool para la obtención de metricas:

## Aspectos preliminares sobre el sflowtool ##

### Descarga e instalación ###

Descargar la herramienta de https://github.com/sflow/sflowtool. Los detalles de como se instala se muestran a continuación.


### Configuración ###

Asumiendo que se tiene una topologia single con el ovs (s1) conectado al controlador (ryu) al puerto 6653 y todos estan corriendo en una misma maquina. La configuración basica para el caso se muestra a continuación:

```bash
${AGENT_IP} = wlp2s0
${COLLECTOR_IP} = 127.0.0.1
${COLLECTOR_PORT} = 6653
${SAMPLING_N} = 10
${POLLING_SECS} = 20
${BRIDGE} = s1

ovs-vsctl -- --id=@sflow create sflow agent=${AGENT_IP} \
    target="\"${COLLECTOR_IP}:${COLLECTOR_PORT}\"" header=${HEADER_BYTES} \
    sampling=${SAMPLING_N} polling=${POLLING_SECS} \
      -- set bridge ${BRIDGE} sflow=@sflow
```

**Nota**: ${AGENT_IP} depende del nombre de la interfaz de red de la maquina usada (por lo menos para el caso del ovs - dudas y muchas al respecto).

En el siguiente [enlace](https://gist.github.com/pichuang/11332074) hay un script que automatiza el proceso.

Para nuestro caso cuando se realiza el reemplazo se tendrá algo como lo siguiente:

```bash
sudo ovs-vsctl -- --id=@sflow create sflow agent=wlp2s0 \
    target="\"127.0.0.1:6653\"" \
    sampling=10 polling=20 \
      -- set bridge s1 sflow=@sflow
```

## Proceso de experimentación ##

1. Arranque el sflow al puerto en cuestion:

```bash
sflowtool -p 6653
```

2. Se arranco la topologia:

```bash
sudo mn --topo=single,3 --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1:6653  --link=tc,bw=100 
```

3. Se configuró el sflow con el ovs y se verificó que todo estuviera bien. Para esto se emplearon los siguientes comandos:


```bash
sudo ovs-vsctl -- --id=@sflow create sflow agent=wlp2s0 \
    target="\"127.0.0.1:6653\"" \
    sampling=10 polling=20 \
      -- set bridge s1 sflow=@sflow

sudo ovs-vsctl list sflow
```

Cuya salida en consola se muestra a continuación:

```bash
tigarto@fuck-pc:~/Documents/tesis_2019-1/tests/febrero/14/controler_apps$ sudo ovs-vsctl -- --id=@sflow create sflow agent=wlp2s0 \
>     target="\"127.0.0.1:6653\"" \
>     sampling=10 polling=20 \
>       -- set bridge s1 sflow=@sflow
844745b8-713f-4c3a-8aa2-842fdf2a8e47
tigarto@fuck-pc:~/Documents/tesis_2019-1/tests/febrero/14/controler_apps$ sudo ovs-vsctl list sflow
_uuid               : 844745b8-713f-4c3a-8aa2-842fdf2a8e47
agent               : "wlp2s0"
external_ids        : {}
header              : []
polling             : 20
sampling            : 10
targets             : ["127.0.0.1:6653"]
tigarto@fuck-pc:~/Documents/tesis_2019-1/tests/febrero/14/controler_apps$ 
```

**Nota**: Si lo que se quiere es remover un sflow de un switch se emplea el siguiente comando:

```bash
ovs-vsctl remove bridge SWITCH_NAME sflow <sFlow UUID>
```

5. Asegurese de estar en un directorio en el cual se encuentren los scripts con las aplicaciones que ejecutará el controlador elegido (en este caso ryu) y una vez alli :

```bash
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
```

6. Ejecute diferentes comandos y observe la salida dada por el sflow. A continuación se muestra un ejemplo de esta:


```bash
...
ifOutBroadcastPkts 4294967295
ifOutDiscards 0
ifOutErrors 0
ifPromiscuousMode 0
endSample   ----------------------
endDatagram   =================================
startDatagram =================================
datagramSourceIP 127.0.0.1
datagramSize 184
unixSecondsUTC 1551998323
localtime 2019-03-07T17:38:43-0500
datagramVersion 5
agentSubId 0
agent 10.1.68.146
packetSequenceNo 2185
sysUpTime 129000
samplesInPacket 1
startSample ----------------------
sampleType_tag 0:2
sampleType COUNTERSSAMPLE
sampleSequenceNo 7
sourceId 0:21
counterBlock_tag 0:1004
openflow_datapath_id 0000000000000001
openflow_port 2
counterBlock_tag 0:1005
ifName s1-eth2
counterBlock_tag 0:1
ifIndex 21
networkType 6
ifSpeed 10000000000
ifDirection 1
ifStatus 3
ifInOctets 996
ifInUcastPkts 12
ifInMulticastPkts 0
ifInBroadcastPkts 4294967295
ifInDiscards 0
ifInErrors 0
ifInUnknownProtos 4294967295
ifOutOctets 4816
ifOutUcastPkts 37
ifOutMulticastPkts 4294967295
ifOutBroadcastPkts 4294967295
ifOutDiscards 0
ifOutErrors 0
ifPromiscuousMode 0
endSample   ----------------------
endDatagram   =================================
...
```

La información adicional la puede encontrar en la [pagina de la herramienta](https://github.com/sflow/sflowtool)

### Otros ejemplos de uso ###


```bash
#
sflowtool -p 6653 -L srcIP,dstIP,inputPort,outputPort
#

```

## Enlaces ##

1. http://www.openvswitch.org/support/ovscon2014/17/1400-ovs-sflow.pdf
2. https://inmon.com/technology/sflowTools.php
3. https://danny270degree.blogspot.com/2012/04/sflow-sflow-agent-and-sflow-collector.html
4. https://danny270degree.blogspot.com/2013/02/sflow-use-sflowtool-to-parse-sflow.html
5. https://inmon.com/technology/sflowTools.php
6. https://github.com/PacktPublishing/Mastering-Python-Networking
7. https://github.com/PacktPublishing/Mastering-Python-for-Networking-and-Security
8. [sample google libro](https://books.google.com.co/books?id=ah9sDwAAQBAJ&pg=PA265&lpg=PA265&dq=sflowtool+tutorial&source=bl&ots=0KN3SZdgXF&sig=ACfU3U3Blj2LmzVr9NRWkzXC0Vz3iuUqZQ&hl=es&sa=X&ved=2ahUKEwigmanS_fDgAhXu01kKHeSRCeIQ6AEwBXoECAUQAQ#v=onepage&q=sflowtool%20tutorial&f=false)

