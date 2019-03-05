## Diseño experimental ##

Para el caso se hará una prueba sencilla con pyDOE


https://statease.github.io/dexpy/example-coffee.html

Example: Coffee Taste Test
Problem Description
A coffee taste test was conducted at the Stat-Ease office to improve the taste of the coffee [1]. This example uses a simplified version of that experiment.

We will look at 5 input factors:

Amount of Coffee (2.5 to 4.0 oz.)
Grind size (8-10mm)
Brew time (3.5 to 4.5 minutes)
Grind Type (Molido vs blade)
Coffee beans (light vs dark)
With one output, or response, variable:

Average overall liking (1-9)
The liking is an average of the scores of a panel of 5 office coffee drinkers.


--

## Ejemplo: Prueba de sabor a café ##

## Descripción del problema ##
Se realizó una prueba de sabor del café en la oficina de Stat-Ease para mejorar el sabor del café [1]. Este ejemplo utiliza una versión simplificada de ese experimento.

Veremos 5 factores de entrada:
* Cantidad de café (2.5 a 4.0 oz.)
* Tamaño de molienda (8-10 mm)
* Tiempo de preparación (3.5 a 4.5 minutos)
* Tipo de molienda (Molido contra cuchilla)
* Granos de café (claro vs oscuro)

Con una salida, o respuesta, variable:
* En general, me gusta (1-9)

El gusto es un promedio de las puntuaciones de un panel de 5 bebedores de café de oficina.


# Diseño experimental

1. Full factorial 2^5

Out[8]: 27
In[9]: ff2n(2)
Out[9]: 
array([[-1., -1.],
       [ 1., -1.],
       [-1.,  1.],
       [ 1.,  1.]])

import pandas as pd
import numpy as np

https://statease.github.io/dexpy/
https://pythonhosted.org/pyDOE/
https://towardsdatascience.com/design-your-engineering-experiment-plan-with-a-simple-python-command-35a6ba52fa35

https://github.com/tirthajyoti/Design-of-experiment-Python/blob/master/DOE_functions.py
https://statease.github.io/dexpy/


