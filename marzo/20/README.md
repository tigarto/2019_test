


```bash
sudo mn --topo=single,3 --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1:6653  --link=tc,bw=100 
```


```bash
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
```


```
bwm-ng -I s1-eht1,s1-eth2,s1-eth3,lo -t 1000
```

```bash
bwm-ng -I s1-eht1,s1-eth2 -o csv -t 1000 > monitoreo_minimal_topo.csv
```

```
hping3 --flood --rand-source 10.0.0.3
```

openflow_v4

openflow_v4.type && tcp.port == 6653

openflow_v4.type == OFPT_PACKET_IN

(openflow_v4.type == OFPT_PACKET_IN)&&(tcp.port==6653) 

(openflow_v4.type == OFPT_PACKET_OUT)&&(tcp.port==6653) 


Statistics > TCP Stream graphs



tshark -r traza2_of.pcap.gz

tshark -r traza2_of.pcap.gz -Y openflow_v4.type && tcp.port == 6653
