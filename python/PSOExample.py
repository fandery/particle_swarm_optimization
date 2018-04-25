"""
Adaptado de: 
@author: edielson - https://github.com/edielsonpf
"""

# Simulador de colonia de passaros na solucao de problemas.
# Baseado no artigo Partical Swarm Optimization de James Kennedy.
#
# Por Edielson Prevato Frigieri

#import sys
#import os.path
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from ParticleSwarmOptimization.pso import pso
import matplotlib.pyplot as plt

if __name__ == '__main__': 
 
    #define as constantes da colonia
    NUM_BIRDS = 50
    NUM_INTERACTIONS = 500
    MAX_SIZE = 10
    MAX_ERRO = 0.1
    NUM_VARS = 3
    
    #OPTION = 'CORNFIELD_VECTOR'
    OPTION = 'NEAREST_NEIGHBOR_VELOCITY_MATCHING'
    
    #Define a posicao da comida aleatoriamente
    roostPoint = np.random.randn(NUM_VARS)*5
    
     
    swarm = pso(NUM_BIRDS,NUM_VARS,NUM_INTERACTIONS,OPTION)
    gbestVal = swarm.search(roostPoint,MAX_ERRO)
    
    interaction=[i for i in range(len(gbestVal))]
    print(interaction)
    
    plt.pause(2)
    plt.plot(interaction,gbestVal)
    plt.show()  
    
