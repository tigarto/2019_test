



1. https://www.bogotobogo.com/python/python_subprocess_module.php
2. https://www.journaldev.com/17416/python-subprocess
3. https://www.tutorialspoint.com/python/os_popen.htm
4. https://www.python-course.eu/os_module_shell.php
5. https://crashcourse.housegordon.org/python-subprocess.html
6. http://dwoll.de/rexrepos/posts/dfSplitMerge.html
7. https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html
8. https://www.datacamp.com/community/tutorials/pandas-split-apply-combine-groupby
9. https://github.com/mininet/mininet/wiki/Teaching-and-Learning-with-Mininet
10. https://wiki.onosproject.org/display/ONOS/Mininet+and+onos.py+workflow
11. http://xmodulo.com/monitor-openflow-messages.html
12. https://stackoverflow.com/questions/45763616/how-to-capture-openflow-packets-using-tshark	
13. http://xmodulo.com/monitor-openflow-messages.html
14. https://wiki.wireshark.org/OpenFlow
15. https://stackabuse.com/pythons-os-and-subprocess-popen-commands/




```bash
bwm-ng -I s1-eth1,s1-eth2,s1-eth3,lo -o csv -t 1000 > monitoreo.csv
```

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


Ademas:

hping3 --flood --rand-source 10.0.0.3
https://github.com/KimiNewt/pyshark
http://yenolam.com/writings/tshark.pdf
http://xmodulo.com/monitor-openflow-messages.html
https://stackoverflow.com/questions/45763616/how-to-capture-openflow-packets-using-tshark
https://wiki.wireshark.org/OpenFlow
https://www.cellstream.com/reference-reading/tipsandtricks/272-t-shark-usage-examples


sudo tshark -i lo -d tcp.port==6653,openflow -O openflow_v4 -w capture-of1.pcap

https://hackertarget.com/tshark-tutorial-and-filter-examples/
https://www.activecountermeasures.com/blog-tshark-examples-for-extracting-ip-fields/
https://linuxsimba.com/tshark-examples
http://yenolam.com/writings/tshark.pdf

https://medium.com/vera-worri/extracting-the-payload-from-tshark-directly-file-using-python-part-ii-994f587075c9


solucion:
https://askubuntu.com/questions/454734/running-wireshark-lua-error-during-loading


https://gist.github.com/sweenzor/1685717

https://www.saltycrane.com/blog/2011/11/how-get-username-home-directory-and-hostname-python/
https://superuser.com/questions/81233/wireshark-permission-problem-in-ubuntu


Veamos si aqui si:
https://superuser.com/questions/81233/wireshark-permission-problem-in-ubuntu


https://osqa-ask.wireshark.org/questions/54690/how-do-i-make-tshark-write-a-pcap-capture-rather-than-a-pcapng-capture

sudo tshark -i lo -w ca_of1.pcap -F libpcap
https://www.dragonjar.org/parseando-pcaps-con-tshark.xhtml


Aqui esta la solucion: http://csie.nqu.edu.tw/smallko/sdn/openflow_pkts.htm

**Marzo 23**:

https://medium.com/@vworri/extracting-the-payload-from-a-pcap-file-using-python-d938d7622d71
https://wiki.wireshark.org/Python
https://kiminewt.github.io/pyshark/
https://github.com/secdev/scapy/blob/master/scapy/contrib/openflow.py
https://github.com/krish7919/openflow-test
https://pdfs.semanticscholar.org/2e7c/8514ab7205f69bfa5e24721a33628ca087ef.pdf
https://www.omicsonline.org/open-access/scapya-python-tool-for-security-testing-jcsb-1000182.pdf
https://scapy.net/conf/scapy_T2.pdf
https://blogs.sans.org/pen-testing/files/2016/04/ScapyCheatSheet_v0.2.pdf