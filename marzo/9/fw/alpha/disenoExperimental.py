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
    ryu_normal.setTopo(TopologiaTest())
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
    ryu_ataque.setTopo(TopologiaTest())
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
    pox_normal.setTopo(TopologiaTest())
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
    pox_ataque.setTopo(TopologiaTest())
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
   ******* Por agregar (CPU, PACKET_IN, PACKET_OUT, FLOW_MOD, Rx..., Tx...)
2. Factores:
   -> Controlador: Ryu, POX
   -> Tipo de trafico: Normal, tasa fija, flooding
      - Normal (background): hping3 -c 6000 IP_V (...)
      - Flooding y spoofing: hping3 ...
3. Numero de tratamientos: 20 tratamientos: 2^2
4. Numero de replicas por tratamiento: 2.   
'''

# En el momento por cuestiones de test solo van a ser dos pruebas

def obtenerTratamientos(niveles):
    num_factores = len(niveles)
    niveles_factor = {}
    for k in niveles:
        niveles_factor[k] = len(niveles[k])
    # print(niveles_factor.keys(),niveles_factor.values())
    tratamientos = fullfact(niveles_factor.values())    
    return tratamientos

def codificarTratamientos(niveles):
    factores = niveles.keys()
    tr = obtenerTratamientos(niveles)
    tr = tr.astype(int)
    tr_cod = tr.astype(str)
    #print(tr_cod)
    num_rows = tr.shape[0]
    i = 0
    index_fac = 0
    index_row = 0
    for e in np.nditer(tr, order='F'):        
        if i < num_rows:
            #e = factores[index_fac][int(e)]
            #print(e)
            
            #ii = int(e)
            #print(type(i))
             
            #e = niveles[factores[index_fac]][e]   
            i += 1  
        else:
            index_row = 0
            i = 0
            index_fac += 1
        # print(niveles[factores[index_fac]][e])
        tr_cod[index_row][index_fac] = niveles[factores[index_fac]][e]
        index_row += 1
        #print(int(e))
    
    #print tr_cod
    return tr_cod

def obtenerNumeroTratamientos(tratamientos):
    return tratamientos.shape[0]

def crearMatrixReplicas(numTratamientos,numReplicasPorTratamiento):
    random.seed() # Semilla para la aleatorizacion para las pruebas
    total_tests = np.arange(1,numTratamientos*numReplicasPorTratamiento + 1) # Lista ordenada de acuerdo al
                                                                             # numero total de replicas
    random.shuffle(total_tests) # Barajando la lista para aleatorizar el orden de las pruebas
    matrixReplicas = total_tests.reshape(numTratamientos,numReplicasPorTratamiento) # Generando la matrix a partir de la lista
    # print(matrixReplicas)
    return matrixReplicas


def definirOrdenTratamientos(matrixReplicas,tratamientos):
    ordenTratamientos = []
    print(tratamientos[0])
    print(matrixReplicas.shape)
    for rep in range(1,matrixReplicas.shape[0]*matrixReplicas.shape[1] + 1):
        index = np.where(matrixReplicas==rep)
        rep += 1
        #print(index)
        #print(index[0])
        #print(tratamientos[index[0]])
        E = tratamientos[index[0]][0].tolist()
        #print(E)
        ordenTratamientos.append(E)
    return ordenTratamientos
        
    """
    for rep in range(1,matrixReplicas.shape[0]*matrixReplicas.shape[1] + 1):
        index = np.where(matrixReplicas==rep)
        rep += 1
        # print(index)
        # print(tratamientos[index[0]][0])
        E = tratamientos[index[0]][0]
        ordenTratamientos.append([E[0],E[1]])
    """


    

"""
tratamientos[:,0][tratamientos[:,0] == '0'] = niveles['controlador'][0]
tratamientos[:,0][tratamientos[:,0] == '1'] = niveles['controlador'][1]
tratamientos[:,1][tratamientos[:,1] == '0'] = niveles['trafico'][0]
tratamientos[:,1][tratamientos[:,1] == '1'] = niveles['trafico'][1]
tratamientos[:,1][tratamientos[:,1] == '2'] = niveles['trafico'][2]
"""
if __name__ == "__main__":
    info("Ensayo")
    niveles = { 'controlador': ['ryu','pox'],
            'trafico': ['normal','ataque1','ataque2']
    }
    tratamientos = obtenerTratamientos(niveles)
    print(tratamientos)
    print(type(tratamientos))
    tr_cod = codificarTratamientos(niveles)
    n_tr = obtenerNumeroTratamientos(tr_cod)
    m = crearMatrixReplicas(n_tr,20)
    ot = definirOrdenTratamientos(m,tr_cod)
    print(ot)






