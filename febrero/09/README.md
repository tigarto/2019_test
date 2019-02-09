# Experimento #
----
## Pruebas basicas ##

### Prueba medicion del ping ###

1. Lanzar el controlador:

```bash
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
```

2. Lanzar el script de mininet:

```bash
sudo python tiempo.py
```

### Prueba medicion del del iperf ###

1. Lanzar el controlador:

```bash
sudo ryu-manager --verbose simple_switch_13.py ofctl_rest.py
```

2. Lanzar el script de mininet:

```bash
sudo python anchobanda.py
```

El resultado en ambos casos será un archivo de salida y su correspondiente version en **csv** para mas facil analisis.

----
## ToDo ##

1. Experimento completo, donde se hagan uso del paquete metricas creado.
2. Prueba lanzando un ataque despues de un tiempo determinado.
3. Documentar.
----
## Doing ##
1. Colocar en el encabezado de los cvs las unidades.
2. Imprimir las estadisticas del ping (obtenidas del metodo que se hizo para ello).
3. Hacer el programa para obtener estadisticas.
----
## Done ##
1. Automatización del ataque y medidas (Muy basico).
2. Pruebas manuales (ver [enlace](https://github.com/tigarto/2019_test/blob/master/febrero/04/README.md))
3. Generando replicas para el ataque
----
## Notas ##
Lo que se lleva no esta libre de bugs.