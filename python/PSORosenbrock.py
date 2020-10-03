"""
Adaptado de: 
@author: edielson - https://github.com/edielsonpf
"""
# Simulador de colonia de passaros na solucao de problemas.
# Baseado no artigo Partical Swarm Optimization de James Kennedy.
#
# Por Edielson Prevato Frigieri

import numpy as np
from ParticleSwarmOptimization.pso_numeric import pso
import matplotlib.pyplot as plt

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def Rosenbrock(x1,x2):
    return (1-x1)**2+100*(x2-x1**2)**2

if __name__ == '__main__': 
 
    #define as constantes da colonia
    NUM_BIRDS = 10
    NUM_INTERACTIONS = 1
    MAX_SIZE = 10
    MAX_ERRO = 0.01
    NUM_VARS = 2
    
    #OPTION = 'CORNFIELD_VECTOR'
    OPTION = 'NEAREST_NEIGHBOR_VELOCITY_MATCHING'
    
    #Define a posicao da comida aleatoriamente
    roostPoint = [1.0,1.0] #Minimo global para a funcao Rosenbrock 
    TARGET = Rosenbrock(roostPoint[0],roostPoint[1])
     
    swarm = pso(NUM_BIRDS,NUM_VARS,NUM_INTERACTIONS,OPTION)
    gbest_val_vec,best_particle,gbest_val = swarm.search(TARGET,MAX_ERRO)
    
    print('Best individual %s' %best_particle)
    print('Best fitness %g' %gbest_val)
    #print(gbestVal)
    
    interaction=[i for i in range(len(gbest_val_vec))]
    #print(interaction)
    
    #plt.pause(1)
    plt.plot(interaction,gbest_val_vec)
    plt.show()  
    
