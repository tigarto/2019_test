### Forma de automatización 2: Creando una subclase a partir de la clase generica Controller ###

Las siguientes pruebas fueron realizadas adaptando la informacion del enlace [http://mininet.org/blog/2013/06/03/automating-controller-startup/](http://mininet.org/blog/2013/06/03/automating-controller-startup/).

El codigo de la subclase ryu se muestra a continuación:

```python
from mininet.node import Controller
from os import environ

class RYU( Controller ):
    def __init__(self, name = 'c0', ryuArgs, **kwargs):
        Controller.__init__(self, name,
                            command = '/usr/local/bin/ryu-manager',
                            cargs='--ofp-tcp-listen-port %s ' + ryuArgs,
                            **kwargs)

controllers={ 'ryu': RYU }
```

## Ejemplo 1 ##


```bash
sudo mn --custom ryu.py --controller ryu
```

El siguiente comando si no me dio:

```bash
sudo mn --custom ryu.py --controller ryu  --topo=single,3 --mac --switch=ovsk,protocols=OpenFlow13 --link=tc,bw=100 
```

https://github.com/mininet/mininet/wiki/Introduction-to-Mininet#extcontrollers

https://mailman.stanford.edu/pipermail/mininet-discuss/2015-July.txt
