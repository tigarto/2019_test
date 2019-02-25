# Framework version alpha #

* **Fecha**: 22/02/2019
* **Objetivo**: Inicio del framework 

## Pasos en el script ##

1. Definir Unidad experimental
2. Configurar el experimento.
3. Arrancar el experimento.
4. Detener la topologia.
5. Detener el controlador.

## Casos de test ##

### Forma 1 ###

El script [unidad_experimental1.py](unidad_experimental1.py) lanza una nueva consola que ejecuta el controlador y posteriormente lanza la consola de mininet (CLI) para ejecutar diferentes comandos. Cuando sale de mininet se limpia la red. El comando de invocación se muestra a continuación:

```bash
sudo python unidad_experimental1.py
```

### Forma 2 ###

El script [unidad_experimental2.py](unidad_experimental2.py) hace lo mismo pero es mediante mininet que se lanzar el controlador (no se despliega consola de este para nada). A continuación se muestra el comando de ejecución.

```bash
sudo python unidad_experimental2.py
```

