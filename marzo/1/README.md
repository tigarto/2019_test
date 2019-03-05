# Experimento #

```bash
sudo python disenoExperimental.py
```

## Problemas ##

1. El programa se bloquea cuando la conexión entre los host se queda abierta ya que el cliente que lleva a cabo la medición y la escritura del archivo se bloquea. Como posible solución se puede agregar una espera activa en un hilo en el programa principal de modo que se haga un kill del cliente del iperf para que se desbloque la ejecución del programa pero de momento no me ocurre nada mas.
2. Aun los archivos log no son definitivos
3. 