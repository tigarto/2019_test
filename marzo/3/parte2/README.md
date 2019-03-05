# Ensayo para monitorización de trafico #

* **Herramienta seleccionada**: bwm-ng

* **Uso**: A continuacuón se muestra el uso que se hará de la herramienta en el caso dado. (Para mas información ver el [manual online](https://www.systutorials.com/docs/linux/man/1-bwm-ng/)

```bash
bwm-ng 
```
## Ejemplos de uso ##

1. Topologia:
   
```bash 
sudo mn
```

2. Comando:

```bash
bwm-ng
```

Resultado de la salida del comando:

```bash
 bwm-ng v0.6 (probing every 0.500s), press 'h' for help
  input: /proc/net/dev type: rate
  |         iface                   Rx                   Tx                Total
  ==============================================================================
          docker0:           0.00 KB/s            0.00 KB/s            0.00 KB/s
          s1-eth1:           0.00 KB/s            0.00 KB/s            0.00 KB/s
      veth2c680fd:           0.00 KB/s            0.00 KB/s            0.00 KB/s
               lo:           0.00 KB/s            0.00 KB/s            0.00 KB/s
          s1-eth2:           0.00 KB/s            0.00 KB/s            0.00 KB/s
           wlp2s0:           0.00 KB/s            0.00 KB/s            0.00 KB/s
  ------------------------------------------------------------------------------
            total:           0.00 KB/s            0.00 KB/s            0.00 KB/s
```

La idea es solo monitorear las de interes:

```bash
bwm-ng -I s1-eht1,s1-eth2
```

```bash 
bwm-ng v0.6 (probing every 0.500s), press 'h' for help
  input: /proc/net/dev type: rate
  /         iface                   Rx                   Tx                Total
  ==============================================================================
          s1-eth1:           0.00 KB/s            0.00 KB/s            0.00 KB/s
          s1-eth2:           0.00 KB/s            0.00 KB/s            0.00 KB/s
  ------------------------------------------------------------------------------
            total:           0.00 KB/s            0.00 KB/s            0.00 KB/s
```

## Otro caso ##

Ojo:

```bash
timestamp;iface_name;bytes_out/s;bytes_in/s;bytes_total/s;bytes_in;bytes_out;packets_out/s;packets_in/s;packets_total/s;packets_in;packets_out;errors_out/s;errors_in/s;errors_in;errors_out\n
```

```bash
bwm-ng -I s1-eht1,s1-eth2 -o csv > monitoreo_minimal_topo.csv
```
pingall
iperf

h1 ping -c 10 h2
exit

monitoreo_minimal_topo.csv  

```csv
1551637455;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637455;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637455;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637455;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637456;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637456;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637456;s1-eth2;406.00;0.00;406.00;0;203;2.00;0.00;2.00;0;1;0.00;0.00;0;0
1551637456;total;406.00;0.00;406.00;0;203;2.00;0.00;2.00;0;1;0.00;0.00;0;0
1551637457;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637457;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
...
1551637489;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637489;total;36893488147419103232.00;36893488147419103232.00;36893488147419103232.00;18446744073669101225;18446744046740663625;36893488147417870336.00;36893488147417878528.00;36893488147416645632.00;18446744073708938738;18446744073708935444;0.00;0.00;0;0
1551637490;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637490;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637491;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551637491;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0

```

Al final se perdieron las interfaces despues del exit. Por otro lado, el despliegue se hace muy rapido. Lo ideal es que la medición se lleve a cabo para nuestro caso cada 1 segundo.

```
bwm-ng -I s1-eth1,s1-eth2 -t 1000
```

Asi la forma general para la configuración de nuestro comando será:

```bash
bwm-ng -I s1-eht1,s1-eth2 -o csv -t 1000 > monitoreo_minimal_topo.csv
```


```csv
1551638196;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638196;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638197;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638197;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638198;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638198;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638240;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638240;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638241;s1-eth2;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638241;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638242;total;18446744073709551616.00;18446744073709551616.00;18446744073709551616.00;18446744073634169283;18446744000660524402;18446744073708027904.00;18446744073708408832.00;18446744073706885120.00;18446744073708409479;18446744073708027206;0.00;0.00;0;0
...
1551638243;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638244;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638245;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638246;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638247;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638248;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638249;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638250;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638251;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638252;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
1551638253;total;0.00;0.00;0.00;0;0;0.00;0.00;0.00;0;0;0.00;0.00;0;0
```


----------------------------------------------

ENlace 1: https://stackoverflow.com/questions/1221555/retrieve-cpu-usage-and-memory-usage-of-a-single-process-on-linux



ps -p <pid> -o %cpu,%mem,cmd


ps -p 1 -o %cpu,%mem,cmd



ps -p 4992 -o %cpu,%mem,cmd
ps -p 5137 -o %cpu,%mem,cmd


ps -C mn -o %cpu,%mem,cmd


https://unix.stackexchange.com/questions/554/how-to-monitor-cpu-memory-usage-of-a-single-process


sudo pip install psrecord


sudo pip install memory_profiler


https://github.com/astrofrog/psrecord

root      4985  0.0  0.0  28352  4068 pts/14   Ss+  13:54   0:00 bash --norc -is mininet:c0
root      4992  0.0  0.0  28352  3944 pts/20   Ss+  13:54   0:00 bash --norc -is mininet:h1
root      4994  0.0  0.0  28352  4024 pts/21   Ss+  13:54   0:00 bash --norc -is mininet:h2
root      4999  0.0  0.0  28356  3932 pts/22   Ss+  13:54   0:00 bash --norc -is mininet:s1
tigarto   7609  0.0  0.0  21296   972 pts/24   S+   14:52   0:00 grep --color=auto mininet


4985
4992
4994
4999

psrecord 4985 --plot plot.png

psrecord 4985 --log activity.txt

psrecord 4985 --log activity.txt --interval 1
