### Forma de automatización 1: Usando la linea de comandos ###

Las siguientes pruebas fueron realizadas adaptando la informacion del enlace [http://mininet.org/blog/2013/06/03/automating-controller-startup/](http://mininet.org/blog/2013/06/03/automating-controller-startup/).

* **Nota**: No olvidar poner las aplicaciones (simple_switch_13.py y ofctl_rest.py para el caso) que invocará el controlador en el directorio desde donde se pasan como argumentos. En este caso se colocaron en el mismo directorio.

## Ejemplo 1 ##

```bash
sudo mn --controller ryu,simple_switch_13.py,ofctl_rest.py
```

## Ejemplo 2 ##

```bash
sudo mn --topo=single,3 --mac --switch=ovsk,protocols=OpenFlow13 --link=tc,bw=100 --controller ryu,simple_switch_13.py,ofctl_rest.py
```

<!---
### The super automatic way #2: creating a custom Controller() subclass ### 


http://mininet.org/blog/2013/06/03/automating-controller-startup/
https://github.com/mininet/openflow-tutorial/wiki
https://github.com/mininet/openflow-tutorial/wiki/Create-a-Learning-Switch
http://mininet.org/blog/page/2/
https://github.com/cgiraldo/minievents
http://mininet.org/walkthrough/
https://github.com/mininet/mininet/wiki/Introduction-to-Mininet


https://github.com/mininet/openflow-tutorial/wiki/Create-a-Learning-Switch

https://www.cs.princeton.edu/courses/archive/fall10/cos561/assignments/ps2-tut.pdf

https://doc.ilabt.imec.be/fgre/_downloads/floodlightcontroller-HowtoWorkwithFast-FailoverOpenFlowGroups-060715-1143-126.pdf
http://www.shihada.com/node/S16-344/assignment1.pdf

https://github.com/hip2b2/poxstuff/blob/master/flow_stats.py





https://moodle.whitireia.ac.nz/mod/book/view.php?id=426702&chapterid=47515

https://github.com/jgjl/bwm-ng/tree/lxns

https://github.com/mininet/mininet/wiki/Teaching-and-Learning-with-Mininet

https://github.com/mininet/mininet/wiki/Simple-Router
https://github.com/mininet/mininet/wiki/Mac-address-table-overflow-attack
https://github.com/mininet/mininet/wiki/Dhcp-masquerade-attack
https://github.com/mininet/mininet/wiki/BGP-Path-Hijacking-Attack-Demo
https://bitbucket.org/jvimal/bgp/src/789055b95a66?at=master

http://conferences.sigcomm.org/co-next/2012/eproceedings/conext/p253.pdf

-->