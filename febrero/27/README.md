# Script para la generacion de la prueba experimental #



**Comando de ejecucion**:

```python
python generadorExperimental.py 
```

**Salida**:

```bash
****************** Tratamientos ******************
  controlador        trafico
0         Ryu  traficoNormal
1         Ryu  traficoAtaque
2         POX  traficoNormal
3         POX  traficoAtaque

****************** Matrix con el orden de experimentacion ******************
[[37 15 17 40  6 11 10 28 24 30]
 [ 7  8  4 20 36 27  2 18 32 31]
 [ 5 12 39  9 16 33 22 34 26 19]
 [ 3 25 13 38 23 35 21 29  1 14]]

****************** Orden de ejecucion de las simulaciones ******************
('POX', 'traficoAtaque')
('POX', 'traficoAtaque')
('Ryu', 'traficoAtaque')
('Ryu', 'traficoAtaque')
('POX', 'traficoAtaque')
('POX', 'traficoAtaque')
('Ryu', 'traficoAtaque')
('Ryu', 'traficoAtaque')
('POX', 'traficoNormal')
('POX', 'traficoNormal')

...

('Ryu', 'traficoAtaque')
('POX', 'traficoNormal')
('POX', 'traficoNormal')
```
