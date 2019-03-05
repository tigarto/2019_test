import dexpy.factorial
import dexpy.power
import dexpy.alias
import pandas as pd
import numpy as np
import dexpy.design
import random
import sys

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
'''
Factores:
1. Controlador (controlador)
2. Tipo de trafico (trafico)

Niveles: 
-> Controlador: 1. ryu
                2. pox
-> Tipo de trafico: 1. normal
                    2. ataque
'''

print "**********************************************************"
print "              PARAMETROS DE CONFIGURACION                 "
numFactores = 2
numNiveles = 2
numReplicasPorTratamiento = 2
print "-> Numero de factores: ",numFactores
print "-> Numero de niveles: ",numNiveles
print "-> Numero de replicas por tratamiento: ",numReplicasPorTratamiento
print
print
# Generando los tratamientos
tratamientos = dexpy.factorial.build_factorial(numFactores, numFactores**numNiveles)
tratamientos.columns = ['controlador', 'trafico']

# Codificacion de los niveles
n1 = { 'controlador': 'ryu', 'trafico': 'normal'}
n2 = { 'controlador': 'pox', 'trafico': 'ataque'}

# Tratamientos codificados
actual_design = dexpy.design.coded_to_actual(tratamientos, n1, n2 )
print("****************** Tratamientos ******************")
print (actual_design)

numTratamientos = actual_design.shape[0] # Numero de tratamientos

random.seed() # Semilla para la aleatorizacion para las pruebas
total_tests = np.arange(1,numTratamientos*numReplicasPorTratamiento + 1) # Lista ordenada de acuerdo al
                                                                         # numero total de replicas
random.shuffle(total_tests) # Barajando la lista para aleatorizar el orden de las pruebas


matrixReplicas = total_tests.reshape(numTratamientos,numReplicasPorTratamiento) # Generando la matrix a partir de la lista
print
print
print("****************** Matrix con el orden de experimentacion ******************")
print(matrixReplicas)

rep = 1
ordenExperimentos = []
ordenTratamientos = []
for i in range(1,numReplicasPorTratamiento*numTratamientos + 1):
    index = np.where(matrixReplicas==rep)
    rep += 1
    E = actual_design.loc[int(index[0])]
    print E.values
    ordenTratamientos.append(E.values)
print(ordenTratamientos)

print
print
print("****************** Orden de ejecucion de las simulaciones ******************")

experimento = {
    "ryu-ataque": {"ping": 0, "iperf":0},
    "ryu-normal": {"ping": 0, "iperf":0},
    "pox-ataque": {"ping": 0, "iperf":0},
    "pox-normal": {"ping": 0, "iperf":0},
}

filenames = []
nameFile = ''
i = 0

for t in ordenTratamientos:
    i += 1
    for test in ["ping", "iperf"]:

        if t[0] == 'ryu':
            # RYU
            if t[1] == 'ataque':
                # RYU - ATAQUE
                nameFile = "ryu-ataque-"
                nameFile += test
                if test == "iperf":
                    experimento["ryu-ataque"]["iperf"] += 1
                    nameFile += "-"+ str(experimento["ryu-ataque"]["iperf"]) + ".log"
                else:
                    experimento["ryu-ataque"]["ping"] += 1
                    nameFile += "-" + str(experimento["ryu-ataque"]["ping"]) + ".log"
            else:
                nameFile = "ryu-normal-"
                nameFile += test
                if test == "iperf":
                    experimento["ryu-normal"]["iperf"] += 1
                    nameFile += "-" + str(experimento["ryu-normal"]["iperf"]) + ".log"
                else:
                    experimento["ryu-normal"]["ping"] += 1
                    nameFile += "-" + str(experimento["ryu-normal"]["ping"]) + ".log"

        else:
            # POX
            if t[1] == 'ataque':
                # POX - ATAQUE
                nameFile = "pox-ataque-"
                nameFile += test
                if test == "iperf":
                    experimento["pox-ataque"]["iperf"] += 1
                    nameFile += "-" + str(experimento["pox-ataque"]["iperf"]) + ".log"
                else:
                    experimento["pox-ataque"]["ping"] += 1
                    nameFile += "-" + str(experimento["pox-ataque"]["ping"]) + ".log"
            else:
                nameFile = "pox-normal-"
                nameFile += test
                if test == "iperf":
                    experimento["pox-normal"]["iperf"] += 1
                    nameFile += "-" + str(experimento["pox-normal"]["iperf"]) + ".log"
                else:
                    experimento["pox-normal"]["ping"] += 1
                    nameFile += "-" + str(experimento["pox-normal"]["ping"]) + ".log"
        filenames.append(nameFile)

print "Total arhivos:", i
print "Experimentos:"
for i in range(0,len(filenames)):
    sys.stdout.write(filenames[i] + "  ")
    if((i+1)%4 == 0):
        print

print
print

