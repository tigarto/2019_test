
## Ejemplo 1 ##


Inicialmente se va a realizar el siguiente ejemplo tomando como base la siguiente pagina: [Port mirroring with Linux bridges](https://backreference.org/2014/06/17/port-mirroring-with-linux-bridges/)

Crear una topologia single de 3 host haciendo que se haga un port-mirror en el puerto s1-eth1 de modo que su trafico de entrada y salida sea llevado al puerto s1-eth3.

1. Crear la topologia:

```bash
sudo mn -topo single,3
net
```

2. Mirar los switches ovs disponibles:

```bash
sudo ovs-vsctl show
```

Salida:
```bash
tigarto@fuck-pc:~$ sudo ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        Controller "ptcp:6634"
        fail_mode: secure
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1"
            Interface "s1"
                type: internal
        Port "s1-eth3"
            Interface "s1-eth3"
        Port "s1-eth1"
            Interface "s1-eth1"
    ovs_version: "2.5.5"
```

3. Mirar informacion asociada al switch:

```bash
sudo ovs-vsctl list bridge s1
```

Salida:

```bash
sudo ovs-vsctl list bridge s1
_uuid               : 0a389068-dfdb-4a18-92d2-801f3deb139e
auto_attach         : []
controller          : [2b7b29e9-2659-49a0-94eb-feeb3b463bda, cc2595c4-ab95-4af8-ad9f-ef8df07d3bb4]
datapath_id         : "0000000000000001"
datapath_type       : ""
datapath_version    : "<unknown>"
external_ids        : {}
fail_mode           : secure
flood_vlans         : []
flow_tables         : {}
ipfix               : []
mcast_snooping_enable: false
mirrors             : []
name                : "s1"
netflow             : []
other_config        : {datapath-id="0000000000000001", disable-in-band="true"}
ports               : [1e32b11d-18b2-4233-91f3-26711b1c9f47, 3e8b8f43-451f-40b8-8571-06ee204701a0, 40989dfb-aec9-445f-a978-4b66b9487dd2, d551794f-c646-449a-8d00-d1cb12e71882]
protocols           : []
rstp_enable         : false
rstp_status         : {}
sflow               : []
status              : {}
stp_enable          : false
```

Viendo los _uuid de cada puerto mas ordenadamente:

```bash
for p in s1-eth{1..3}; do echo "$p: $(sudo ovs-vsctl get port "$p" _uuid)"; done
```

Salida:


```bash
for p in s1-eth{1..3}; do echo "$p: $(sudo ovs-vsctl get port "$p" _uuid)"; done
s1-eth1: d551794f-c646-449a-8d00-d1cb12e71882
s1-eth2: 1e32b11d-18b2-4233-91f3-26711b1c9f47
s1-eth3: 40989dfb-aec9-445f-a978-4b66b9487dd2
```

4. Creacion de los port-mirrors: A continuación se muestra el proceso de creación paso a paso:
   i.  Crear y añadir un port mirror al bridge:

   ```bash
   sudo ovs-vsctl -- --id=@m create mirror name=mymirror -- add bridge s1 mirrors @m
   ```

   Salida:

   ```bash
   sudo ovs-vsctl -- --id=@m create mirror name=mymirror -- add bridge s1 mirrors @m
   bb5e48dd-49f7-4829-a4cd-611cd732f264
   ```

   ii. Comprobar que el mirror se creo:

   ```bash
   sudo ovs-vsctl list bridge s1
   ```

    Salida:

   ```bash
   sudo ovs-vsctl list bridge s1
   _uuid            :0a389068-dfdb-4a18-92d2-801f3deb139e
   auto_attach         : []
   controller      :2b7b29e9-2659-49a0-94eb-feeb3b463bda, cc2595c4-ab95-4af8-ad9f-ef8df07d3bb4]
   datapath_id         : "0000000000000001"
   datapath_type       : ""
   datapath_version    : "<unknown>"
   external_ids        : {}
   fail_mode           : secure
   flood_vlans         : []
   flow_tables         : {}
   ipfix               : []
   mcast_snooping_enable: false
   mirrors       : [bb5e48dd-49f7-4829-a4cd-611cd732f264]
   name                : "s1"
   netflow             : []
   other_config    : {datapath-id="0000000000000001", disable-in-band="true"}
   ports         : [1e32b11d-18b2-4233-91f3-26711b1c9f47, 3e8b8f43-451f-40b8-8571-06ee204701a0, 40989dfb-aec9-445f-a978-4b66b9487dd2, d551794f-c646-449a-8d00-d1cb12e71882]
   protocols           : []
   rstp_enable         : false
   rstp_status         : {}
   sflow               : []
   status              : {}
   stp_enable          : false
   ```

   iii. Agregar los **puntos de origen** los cuales se definen como los puertos cuyo trafico se desea mirroring.

   * **Para hacer mirror del trafico de salida del puerto en cuestion**: select_scr_port

   ```bash
   sudo ovs-vsctl -- --id=@s1-eth1 get port s1-eth1 -- set mirror mymirror select_src_port=@s1-eth1 select_dst_port=@s1-eth1
   ```

   Luego se verifica:

   ```bash
   sudo ovs-vsctl list mirror mymirror
   _uuid              : bb5e48dd-49f7-4829-a4cd-611cd732f264
   external_ids        : {}
   name                : mymirror
   output_port         : []
   output_vlan         : []
   select_all          : false
   select_dst_port     : [d551794f-c646-449a-8d00-d1cb12e71882]
   select_src_port     : [d551794f-c646-449a-8d00-d1cb12e71882]
   select_vlan         : []
   statistics          : {}
   ```

 *  **Para hacer mirror del trafico de entrada del puerto en cuestion**: select_dst_port

 
```bash
sudo ovs-vsctl -- --id=@s1-eth3 get port s1-eth3 -- set mirror mymirror output-port=@s1-eth3
```
Luego se verifica:

   ```bash
   sudo ovs-vsctl list mirror mymirror
_uuid               : bb5e48dd-49f7-4829-a4cd-611cd732f264
external_ids        : {}
name                : mymirror
output_port         : 40989dfb-aec9-445f-a978-4b66b9487dd2
output_vlan         : []
select_all          : false
select_dst_port     : [d551794f-c646-449a-8d00-d1cb12e71882]
select_src_port     : [d551794f-c646-449a-8d00-d1cb12e71882]
select_vlan         : []
statistics          : {tx_bytes=0, tx_packets=0}
   ```

5. Remosión de un port mirror especifico:

```bash
ovs-vsctl -- --id=@m get mirror mymirror -- remove bridge s1 mirrors @m
```

Verificando:

```bash
sudo ovs-vsctl list mirror mymirror
ovs-vsctl: no row "mymirror" in table Mirror
```

6. Removiendo todos los mirrors:

```bash
ovs-vsctl clear bridge s1 mirrors
```

**Tips**

1. **Tip 1**: Creación y configuración de un port mirror en un solo comando:

```bash
sudo ovs-vsctl \
  -- --id=@m create mirror name=mymirror \
  -- add bridge s1 mirrors @m \
  -- --id=@s1-eth1 get port s1-eth1 \
  -- set mirror mymirror select_src_port=@s1-eth1 select_dst_port=@s1-eth1 \
  -- --id=@s1-eth3 get port s1-eth3 \
  -- set mirror mymirror output-port=@s1-eth3
```

Salida:

```bash 
sudo ovs-vsctl   -- --id=@m create mirror name=mymirror   -- add bridge s1 mirrors @m   -- --id=@s1-eth1 get port s1-eth1   -- set mirror mymirror select_src_port=@s1-eth1 select_dst_port=@s1-eth1   -- --id=@s1-eth3 get port s1-eth3   -- set mirror mymirror output-port=@s1-eth3
cb396ec0-f27c-4f56-aadc-be1db7b3e03b
```

Comprobación:

```bash
sudo ovs-vsctl list mirror mymirror
_uuid               : cb396ec0-f27c-4f56-aadc-be1db7b3e03b
external_ids        : {}
name                : mymirror
output_port         : 142105f2-e137-4ff8-ae92-dfae25ea06eb
output_vlan         : []
select_all          : false
select_dst_port     : [2634b475-269b-4945-a95d-32eaef906103]
select_src_port     : [2634b475-269b-4945-a95d-32eaef906103]
select_vlan         : []
statistics          : {tx_bytes=0, tx_packets=0}
```

1. **Tip 2**: Forma aun mas consisa si se quisiera port mirror desde todos los puertos:

Forma 1:

```bash
ovs-vsctl \
  -- --id=@vnet0 get port s1-eth1 \
  -- --id=@vnet1 get port s1-eth2 \
  -- set mirror mymirror 'select_src_port=[@s1-eth1,@s1-eth2]' 'select_dst_port=[@s1-eth1,@s1-eth2]'

ovs-vsctl -- --id=@s1-eth3 get port s1-eth3 -- set mirror mymirror output-port=@s1-eth3
```

Forma 2 - Aun mas consisa:

```bash
ovs-vsctl -- --id=@s1-eth3 get port s1-eth3 -- set mirror mymirror select_all=true output-port=@s1-eth3
```

### Resumen ###

En la pagina [Monitoring OpenvSwitch Ports](http://www.stackguy.com/archives/138) se muestra la sintaxis de un comando tipico de los anteriormente vistos:

```bash
ovs-vsctl --- set Bridge <bridge-name> mirrors=@m --- --id=@mon0 \
get Port mon0 --- --id=@<port-name> get Port <port-name> \
--- --id=@m create Mirror name=mymirror select-dst-port=@<port-name> \
select-src-port=@<port-name> output-port=@mon0 select_all=1
```

### Ejemplo pagina de smallko - Openvswitch Port Mirroring ###

En la pagina [Openvswitch Port Mirroring](http://csie.nqu.edu.tw/smallko/sdn/port-mirroring.htm) se encuentra el ejemplo.

  There are three hosts, i.e. h1, h2, h3, that are connecting to an openvswitch(s1). We want the port 3 (connecting to h3) to be the mirroring port that can monitor the traffic between h1 and h2.

El archivo de topologia es [port-mirroring.py](port-mirroring.py) 

Se procedio a ejecutar y el resultado fue el esperado. A continuación se muestran los comandos ejecutados en cada terminal en su orden aproximado:

**bash**

```bash
sudo python port-mirroring.py
```

**Teminal s1**

```bash
ovs-vsctl del-port s1-eth3
sudo ovs-vsctl list bridge s1
ovs-vsctl add-port s1 s1-eth3 -- --id=@p get port s1-eth3 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m
sudo ovs-vsctl list mirror m0
```

**Terminal h3**

```bash
tcpdump
```

**Mininet**

```bash
h1 ping -c 3 h2
```

Finalmente, como dice Smallko: "With this feature, we can install machine learning, IDS/IPS or other mechanism for traffic analysis in h3."


## Referencias ##

* https://arthurchiao.github.io/blog/trafic-mirror-with-ovs/
* http://www.openvswitch.org/support/dist-docs/ovs-tcpdump.8.txt
* http://manpages.ubuntu.com/manpages/bionic/man8/ovs-tcpdump.8.html
* http://www.stackguy.com/archives/138
* https://n40lab.wordpress.com/2013/02/23/openvswitch-port-mirroring/
* https://www.rsreese.com/network-traffic-capture-on-linux-using-openvswitch/
* http://networkstatic.net/openflow-tutorial-lab-3/
* https://software.intel.com/en-us/articles/deploy-an-sdn-wiredwireless-network-with-open-vswitch-ovs-and-faucet
