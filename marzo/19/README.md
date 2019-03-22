# sFLOW #




```bash
sudo mn --topo=single,3 --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1:6653  --link=tc,bw=100 
```

```
sudo ovs-vsctl -- --id=@sflow create sflow agent=wlp2s0 \
    target="\"127.0.0.1:6653\"" \
    sampling=10 polling=20 \
      -- set bridge s1 sflow=@sflow

sudo ovs-vsctl list sflow
```


```bash
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
```

Veamos una salida tipica:

```bash

sflowtool -p 6653
startDatagram =================================
datagramSourceIP 127.0.0.1
datagramSize 188
unixSecondsUTC 1553109482
localtime 2019-03-20T14:18:02-0500
datagramVersion 5
agentSubId 0
agent 10.1.87.159
packetSequenceNo 795
sysUpTime 120000
samplesInPacket 1
startSample ----------------------
sampleType_tag 0:1
sampleType FLOWSAMPLE
sampleSequenceNo 4602
sourceId 2:1000
meanSkipCount 10
samplePool 46020
dropEvents 0
inputPort 25
outputPort dropCode 256
flowBlock_tag 0:1001
extendedType SWITCH
in_vlan 0
in_priority 0
out_vlan 0
out_priority 0
flowBlock_tag 0:1
flowSampleType HEADER
headerProtocol 1
sampledPacketSize 74
strippedBytes 4
headerLen 70
headerBytes 33-33-00-00-00-02-00-00-00-00-00-03-86-DD-60-00-00-00-00-10-3A-FF-FE-80-00-00-00-00-00-00-02-00-00-FF-FE-00-00-03-FF-02-00-00-00-00-00-00-00-00-00-00-00-00-00-02-85-00-7B-28-00-00-00-00-01-01-00-00-00-00-00-03
dstMAC 333300000002
srcMAC 000000000003
IPSize 56
IPTOS 0
IP6_label 0x0
IPV6_payloadLen 16
IPTTL 255
srcIP6 fe80
dstIP6 ff02
IPProtocol 58
endSample   ----------------------
endDatagram   =================================
startDatagram =================================
datagramSourceIP 127.0.0.1
datagramSize 316
unixSecondsUTC 1553109487
localtime 2019-03-20T14:18:07-0500
datagramVersion 5
agentSubId 0
agent 10.1.87.159
packetSequenceNo 796
sysUpTime 125000
samplesInPacket 2
startSample ----------------------
sampleType_tag 0:2
sampleType COUNTERSSAMPLE
sampleSequenceNo 7
sourceId 2:1000
counterBlock_tag 0:2203
user_time 726
system_time 591
memory_used 34496512
memory_max 0
files_open 0
files_max 0
connections_open 0
connections_max 0
counterBlock_tag 0:2207
OVS_dp_hits 15769
OVS_dp_misses 117
OVS_dp_lost 0
OVS_dp_mask_hits 24586
OVS_dp_flows 1
OVS_dp_masks 2
endSample   ----------------------
startSample ----------------------
sampleType_tag 0:1
sampleType FLOWSAMPLE
sampleSequenceNo 4603
sourceId 2:1000
meanSkipCount 10
samplePool 46030
dropEvents 0
inputPort 21
outputPort 25
flowBlock_tag 0:1001
extendedType SWITCH
in_vlan 0
in_priority 0
out_vlan 0
out_priority 0
flowBlock_tag 0:1
flowSampleType HEADER
headerProtocol 1
sampledPacketSize 102
strippedBytes 4
headerLen 98
headerBytes 00-00-00-00-00-03-00-00-00-00-00-01-08-00-45-00-00-54-A3-ED-40-00-40-01-82-B8-0A-00-00-01-0A-00-00-03-08-00-30-54-2A-06-00-01-EE-91-92-5C-00-00-00-00-59-E3-04-00-00-00-00-00-10-11-12-13-14-15-16-17-18-19-1A-1B-1C-1D-1E-1F-20-21-22-23-24-25-26-27-28-29-2A-2B-2C-2D-2E-2F-30-31-32-33-34-35-36-37
dstMAC 000000000003
srcMAC 000000000001
IPSize 84
ip.tot_len 84
srcIP 10.0.0.1
dstIP 10.0.0.3
IPProtocol 1
IPTOS 0
IPTTL 64
IPID 60835
ICMPType 8
ICMPCode 0
endSample   ----------------------
endDatagram   =================================
startDatagram =================================
datagramSourceIP 127.0.0.1
datagramSize 184
unixSecondsUTC 1553109490
localtime 2019-03-20T14:18:10-0500
datagramVersion 5
agentSubId 0
agent 10.1.87.159
packetSequenceNo 797
sysUpTime 128000
samplesInPacket 1
startSample ----------------------
sampleType_tag 0:2
sampleType COUNTERSSAMPLE
sampleSequenceNo 7
sourceId 0:23
counterBlock_tag 0:1004
openflow_datapath_id 0000000000000001
openflow_port 2
counterBlock_tag 0:1005
ifName s1-eth2
counterBlock_tag 0:1
ifIndex 23
networkType 6
ifSpeed 10000000000
ifDirection 1
ifStatus 3
ifInOctets 1948
ifInUcastPkts 24
ifInMulticastPkts 0
ifInBroadcastPkts 4294967295
ifInDiscards 0
ifInErrors 0
ifInUnknownProtos 4294967295
ifOutOctets 7150
ifOutUcastPkts 66
ifOutMulticastPkts 4294967295
ifOutBroadcastPkts 4294967295
ifOutDiscards 0
ifOutErrors 0
ifPromiscuousMode 0
endSample   ----------------------
endDatagram   =================================
startDatagram =================================
datagramSourceIP 127.0.0.1
datagramSize 292
unixSecondsUTC 1553109492
localtime 2019-03-20T14:18:12-0500
datagramVersion 5
agentSubId 0
agent 10.1.87.159
packetSequenceNo 798
sysUpTime 130000
samplesInPacket 2
startSample ----------------------
sampleType_tag 0:1
sampleType FLOWSAMPLE
sampleSequenceNo 4604
sourceId 2:1000
meanSkipCount 10
samplePool 46040
dropEvents 0
inputPort 23
outputPort 21
flowBlock_tag 0:1001
extendedType SWITCH
in_vlan 0
in_priority 0
out_vlan 0
out_priority 0
flowBlock_tag 0:1
flowSampleType HEADER
headerProtocol 1
sampledPacketSize 46
strippedBytes 4
headerLen 42
headerBytes 00-00-00-00-00-01-00-00-00-00-00-02-08-06-00-01-08-00-06-04-00-01-00-00-00-00-00-02-0A-00-00-02-00-00-00-00-00-00-0A-00-00-01
dstMAC 000000000001
srcMAC 000000000002
endSample   ----------------------
startSample ----------------------
sampleType_tag 0:1
sampleType FLOWSAMPLE
sampleSequenceNo 4605
sourceId 2:1000
meanSkipCount 10
samplePool 46050
dropEvents 0
inputPort 25
outputPort 23
flowBlock_tag 0:1001
extendedType SWITCH
in_vlan 0
in_priority 0
out_vlan 0
out_priority 0
flowBlock_tag 0:1
flowSampleType HEADER
headerProtocol 1
sampledPacketSize 46
strippedBytes 4
headerLen 42
headerBytes 00-00-00-00-00-02-00-00-00-00-00-03-08-06-00-01-08-00-06-04-00-02-00-00-00-00-00-03-0A-00-00-03-00-00-00-00-00-02-0A-00-00-02
dstMAC 000000000002
srcMAC 000000000003
endSample   ----------------------
endDatagram   =================================
^C

```

## Referencias ##


1. https://tools.ietf.org/html/draft-ietf-bmwg-sdn-controller-benchmark-term-06#page-5
2. https://tools.ietf.org/html/draft-ietf-bmwg-sdn-controller-benchmark-meth-06
3. https://blog.sflow.com/2012/05/software-defined-networking.html
4. https://blog.sflow.com/2013/05/software-defined-analytics.html
5. https://github.com/tyjhart/flowanalyzer/blob/master/sFlow.md
6. https://core.ac.uk/download/pdf/67578014.pdf
7. http://itas2015.iitp.ru/pdf/1570195931.pdf
8. https://github.com/sflow/sflowtool
9. https://blog.sflow.com/2011/12/sflowtool.html
10. https://blog.sflow.com/2012/01/forwarding-using-sflowtool.html
11. https://hub.docker.com/r/sflow/sflowtool/
12. https://support.solarwinds.com/Success_Center/Netflow_Traffic_Analyzer_(NTA)/Knowledgebase_Articles/Breaking_down_sFlow_packet_in_Wireshark
13. https://inmon.com/technology/sflowTools.php
14. https://inmon.com/pdf/sFlowBilling.pdf
15. https://sflow.org/developers/diagrams/sFlowV5Sample.pdf
16. http://support.huawei.com/enterprise/docinforeader!loadDocument1.action?contentId=DOC1000069596&partNo=10152
17. https://blog.sflow.com/2009/06/sampling-rates.html  
18. https://books.google.com.co/books?id=Jng5DwAAQBAJ&pg=PA229&lpg=PA229&dq=packetin+sflow&source=bl&ots=pOVe0sf6HY&sig=ACfU3U3BbYtdzB72EcimRTJtV9JwC2AIcA&hl=es&sa=X&ved=2ahUKEwiTyKKu7JHhAhUorlkKHeuTDns4ChDoATABegQIBxAB#v=onepage&q=packetin%20sflow&f=false
19. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4781982/
20. 