# Comparación entre ping normal y de ataque #

Solo se emplearan los archivos de salida:

## Normal ##

**RYU**

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.047 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.071 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.084 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.084 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.036 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.054 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.064 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9212ms
rtt min/avg/max/mdev = 0.036/0.068/0.084/0.020 ms
```

**POX**

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.047 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.071 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.084 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.084 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.083 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.036 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.054 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.064 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9212ms
rtt min/avg/max/mdev = 0.036/0.068/0.084/0.020 ms
```

## Ataque ##

**RYU**

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.065 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.025 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.031 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.032 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.028 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.020 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.023 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.024 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.028 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.022 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9214ms
rtt min/avg/max/mdev = 0.020/0.029/0.065/0.014 ms

```

**POX**

```
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.159 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.044 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.041 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.042 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.037 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.084 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.039 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.037 ms

--- 10.0.0.3 ping statistics ---
10 packets transmitted, 8 received, 20% packet loss, time 9206ms
rtt min/avg/max/mdev = 0.037/0.060/0.159/0.040 ms
```
