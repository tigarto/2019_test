import os
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from mininet.topo import Topo
import subprocess
from time import time, sleep
import psutil
from mininet.cli import CLI
from subprocess import Popen, PIPE, STDOUT
from select import poll, POLLIN
from trafico import TraficoAtaque, TraficoNormal
from unidadExperimental import UnidadExperimental
from topologia import TopologiaPOX, TopologiaRyu, TopologiaTest
from controlador import RYU, POX
from experimento import Experimento
import dexpy.factorial
import dexpy.power
import dexpy.alias
import pandas as pd
import numpy as np
from pyDOE import fullfact
import random



""" Caso Ryu-Normal """
def experimentoRyuNormal():
    # Unidad experimental
    ryu_normal = UnidadExperimental()
    ryu_normal.setTopo(topologias['topoTest'])
    ryu_normal.setController('ryu')
    ryu_normal.definirNodosClaves(C = 'h2', V = 'h3')
    # Experimento
    exp_ryu_normal = Experimento()
    exp_ryu_normal.configureParams(ryu_normal)
    exp_ryu_normal.configurarTrafico('normal')
    return exp_ryu_normal

""" Caso Ryu-Ataque """
def experimentoRyuAtaque():
    # Unidad experimental
    ryu_ataque = UnidadExperimental()
    ryu_ataque.setTopo(topologias['topoTest'])
    ryu_ataque.setController('ryu')
    ryu_ataque.definirNodosClaves(A = 'h1',C = 'h2', V = 'h3')
    # Experimento
    exp_ryu_ataque = Experimento()
    exp_ryu_ataque.configureParams(ryu_ataque)
    exp_ryu_ataque.configurarTrafico('ataque')
    return exp_ryu_ataque

""" Caso POX-Normal """
def experimentoPOXNormal():
    # Unidad experimental
    pox_normal = UnidadExperimental()
    pox_normal.setTopo(topologias['topoTest'])
    pox_normal.setController('pox')
    pox_normal.definirNodosClaves(C = 'h2', V = 'h3')
    # Experimento
    exp_pox_normal = Experimento()
    exp_pox_normal.configureParams(pox_normal)
    exp_pox_normal.configurarTrafico('normal')
    return exp_pox_normal

""" Caso POX-Ataque """
def experimentoPOXAtaque():
    # Unidad experimental
    pox_ataque = UnidadExperimental()
    pox_ataque.setTopo(topologias['topoTest'])
    pox_ataque.setController('pox')
    pox_ataque.definirNodosClaves(A = 'h1',C = 'h2', V = 'h3')
    
    # Experimento
    exp_pox_ataque = Experimento()
    exp_pox_ataque.configureParams(pox_ataque)
    exp_pox_ataque.configurarTrafico('ataque')
    return exp_pox_ataque


""" Configuracion de los parametros del disenho experimental"""

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
4. Numero de replicas por tratamiento: 2.   
'''

# En el momento por cuestiones de test solo van a ser dos pruebas

def experimentos(numReplicasPorTratamiento = 2):

    # Parametros del experimento
    numNivelesFactor1 = 2
    numNivelesFactor2 = 3    
    

    # Generando los tratamientos
    tratamientos = fullfact([numNivelesFactor1,numNivelesFactor2])
    #tratamientos.columns = ['controlador', 'trafico']

    # Codificacion de los niveles

    niveles = { 'controlador': { 0:'ryu', 1:'pox'},
                 'trafico': { 0:'normal', 1:'ataque1', 2:'ataque2'}
    }
    

    tratamientos = tratamientos.astype(int)
    tratamientos = tratamientos.astype(str)
    
    
    # Definiendo los tratamientos
    tratamientos[:,0][tratamientos[:,0] == '0'] = niveles['controlador'][0]
    tratamientos[:,0][tratamientos[:,0] == '1'] = niveles['controlador'][1]
    tratamientos[:,1][tratamientos[:,1] == '0'] = niveles['trafico'][0]
    tratamientos[:,1][tratamientos[:,1] == '1'] = niveles['trafico'][1]
    tratamientos[:,1][tratamientos[:,1] == '2'] = niveles['trafico'][2]

    print("****************** Tratamientos ******************")
    print (tratamientos)

    numTratamientos = tratamientos.shape[0] # Numero de tratamientos
    # print(tratamientos[0,0])
    # print(numTratamientos)

    random.seed() # Semilla para la aleatorizacion para las pruebas
    total_tests = np.arange(1,numTratamientos*numReplicasPorTratamiento + 1) # Lista ordenada de acuerdo al
                                                                             # numero total de replicas
    random.shuffle(total_tests) # Barajando la lista para aleatorizar el orden de las pruebas
    matrixReplicas = total_tests.reshape(numTratamientos,numReplicasPorTratamiento) # Generando la matrix a partir de la lista
    # print(matrixReplicas)

    print
    print    
    print("****************** Matrix con el orden de experimentacion ******************")
    print(matrixReplicas)


    ordenTratamientos = []
    for rep in range(1,numReplicasPorTratamiento*numTratamientos + 1):
        index = np.where(matrixReplicas==rep)
        rep += 1
        # print(index)
        # print(tratamientos[index[0]][0])
        E = tratamientos[index[0]][0]
        ordenTratamientos.append([E[0],E[1]])

    print(ordenTratamientos)
    print
    print
    print("****************** Orden de ejecucion de las simulaciones ******************")
    for e in ordenTratamientos:
        print e
        


    

    


    
    filenames = []
    nameFile = ''
    i = 0
    """

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
    

    """
    return filenames

def imprimirArchivosLogGenerados(listaF, num_ren = 4):
    for i in range(0,len(listaF)):
        sys.stdout.write(listaF[i] + "  ")
        if((i+1)%num_ren == 0):
            print
    return len(listaF)

#filesLog = experimentos()
#tam = imprimirArchivosLogGenerados(filesLog)
#print(tam)


if __name__ == "__main__":
    setLogLevel("info")
    files_log = experimentos()
    imprimirArchivosLogGenerados(files_log)
    # files_log = ["pox-ataque-iperf-1.log", "pox-ataque-iperf-2.log"]
    """

    for fl_name in files_log:
        print (fl_name + "\n")
        fl = fl_name.strip('.log')
        test = fl.split('-')[:3]
        if test[0] == 'ryu':
            # RYU
            print('\n*******' + fl_name + '*******')
            if test[1] == 'normal':
                # RYU-NORMAL
                ryu_normal = experimentoRyuNormal()
                sleep(5) # Dando tiempo de construccion
                if test[2] == 'iperf':
                    # RYU-NORMAL-IPERF
                    ryu_normal.startTest()
                    sleep(10)
                    ryu_normal.trafico.iperfMeasure(filename=fl_name, tiempo = 20)
                    ryu_normal.endTest()
                else:
                    # RYU-NORMAL-PING
                    ryu_normal.startTest()
                    sleep(10)
                    ryu_normal.trafico.pingMeasure(filename=fl_name, veces = 20)
                    ryu_normal.endTest()
                ryu_normal.killTest()
                ryu_normal.killController()
            else:
                # RYU-ATAQUE
                ryu_ataque = experimentoRyuAtaque()
                sleep(5) # Dando tiempo de construccion
                if test[2] == 'iperf':
                    # RYU-NORMAL-IPERF
                    ryu_ataque.startTest()
                    sleep(10)
                    ryu_ataque.trafico.iperfMeasure(filename=fl_name, tiempo = 20)
                    ryu_ataque.endTest()
                else:
                    # RYU-NORMAL-PING
                    ryu_ataque.startTest()
                    sleep(10)
                    ryu_ataque.trafico.pingMeasure(filename=fl_name, veces = 20)
                    ryu_ataque.endTest()
                ryu_ataque.killTest()
                ryu_ataque.killController()
        else:           
            # POX
            print('\n*******' + fl_name + '*******')
            if test[1] == 'normal':
                # POX-NORMAL                
                pox_normal = experimentoPOXNormal()
                sleep(5)
                # Dando tiempo de construccion
                if test[2] == 'iperf':
                    # POX-NORMAL-IPERF
                    pox_normal.startTest()
                    sleep(10)
                    pox_normal.trafico.iperfMeasure(filename=fl_name, tiempo = 20)
                    pox_normal.endTest()
                else:
                    # POX-NORMAL-PING
                    pox_normal.startTest()
                    sleep(10)
                    pox_normal.trafico.pingMeasure(filename=fl_name, veces = 20)
                    pox_normal.endTest()
                pox_normal.killTest()
                pox_normal.killController()
            else:
                sleep(10)
                # POX-ATAQUE
                pox_ataque = experimentoPOXAtaque()  
                sleep(5)          
                if test[2] == 'iperf':                    
                    # RYU-NORMAL-IPERF
                    pox_ataque.startTest()
                    sleep(10)
                    pox_ataque.trafico.iperfMeasure(filename=fl_name, tiempo = 20)
                    pox_ataque.endTest()
                else:                    
                    # RYU-NORMAL-PING
                    pox_ataque.startTest()
                    sleep(10)
                    pox_ataque.trafico.pingMeasure(filename=fl_name, veces = 20)
                    pox_ataque.endTest()
                pox_ataque.killTest()
                pox_ataque.killController()            
        
        info("\n******* Experimento finalizado *******\n\n")
        for i in range(10):
            print('.')
            sleep(1)
        print()
        info("\n******* Pasando al siguiente experimento *******\n\n")
    """
    print ("FIN EXPERIMENTOS")



