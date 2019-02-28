import dexpy.factorial
import dexpy.power
import dexpy.alias
import pandas as pd
import numpy as np
import dexpy.design
import random

'''
Descripcion del experimento

1. Variables respuesta:
   -> BW: ancho de banda
   -> RTT_avg 
   -> PacketLoss
2. Factores:
   -> Controlador: Ryu, POX
   -> Tipo de trafico: Normal, tasa fija, flooding
      - Normal (background): hping3 -c 6000 IP_V
      - Flooding y spoofing: hping3 ...
3. Numero de tratamientos: 20 tratamientos: 2^2
4. Numero de replicas por tratamiento: 10.   
'''



# Tratamientos sin codificar
tratamientos = dexpy.factorial.build_factorial(2, 2**2)
tratamientos.columns = ['controlador', 'trafico']
#print(tratamientos)
#print(tratamientos.values)

f1 = { 'controlador': 'Ryu', 'trafico': 'traficoNormal'}
f2 = { 'controlador': 'POX', 'trafico': 'traficoAtaque'}

# Tratamientos codificados
actual_design = dexpy.design.coded_to_actual(tratamientos, f1, f2 )
print("****************** Tratamientos ******************")
print (actual_design)

numTratamientos = actual_design.shape[0]
#print(numTratamientos)

numReplicasPorTratamiento = 10
random.seed()

total_tests = np.arange(1,numTratamientos*numReplicasPorTratamiento + 1)
#print(total_tests)
random.shuffle(total_tests)


matrixReplicas = total_tests.reshape(numTratamientos,numReplicasPorTratamiento)
print
print("****************** Matrix con el orden de experimentacion ******************")
print(matrixReplicas)

rep = 1
ordenExperimentos = []
ordenTratamientos = []
# print (type(actual_design))
# print('\n')
for i in range(numTratamientos*numReplicasPorTratamiento):
    index = np.where(matrixReplicas==rep)
    rep += 1
    #print(index)
    #print(actual_design.loc[int(index[0])])
    E = actual_design.loc[int(index[0])]
    ordenTratamientos.append(actual_design.loc[int(index[0])])
    #print([E['controlador'],E['trafico']])
    ordenTratamientos.append([E['controlador'],E['trafico']])
    ordenExperimentos.append(int(index[0]))

# Aleatorizar evaluacion
# print(ordenExperimentos)
# print (ordenTratamientos)
print
print("****************** Orden de ejecucion de las simulaciones ******************")
for t in ordenTratamientos:
    print(t[0],t[1])

