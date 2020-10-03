"""
Adaptado de: 
@author: edielson - https://github.com/edielsonpf
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

class pso(object):
    '''
    classdocs
    '''


    def __init__(self, num_particles,num_vars,max_interactions,option='CORNFIELD_VECTOR'):
        '''
        Constructor
        '''
        self.num_particles = num_particles
        
        self.num_vars = num_vars
        
        self.max_num_interactions = max_interactions
        
        if (option == 'NEAREST_NEIGHBOR_VELOCITY_MATCHING'):
            self.option = 1
        else: #'CORNFIELD_VECTOR'
            self.option = 2
    
    def __distEuclidean(self,p1,p2):
        
        dist=0
        for var in range(self.num_vars):
            dist=dist+(p1[var]-p2[var])**2
        return np.sqrt(dist)
    
    
    def __nearest(self,particles):
 
        nearests = np.zeros(self.num_particles, dtype=int)
        
        for particle in range(self.num_particles):                   #Para cada passaro do bando.
            #Calcula a distancia euclidiana para cada um dos outros passaros e
            #identifica o passaro que esta mais proximo.
            best = np.inf
            
            for other_particle in range(self.num_particles):             #para todos os passaros
                if other_particle != particle:           #exceto ele mesmo
                    #Calcula a distancia euclidiana.
                    dist = self.__distEuclidean(particles[other_particle],particles[particle])
                    if best > dist:     #Se e menor que a ja existente
                        nearests[particle]=other_particle
                        best = dist;
                    
#             if best > 1:
#                 nearests[particle]=particle
        
        return nearests    

    def __velocityMatching(self,particles,velocities):
 
        nears = self.__nearest(particles)        
        for particle in range(self.num_particles):
            for var in range(self.num_vars):
                velocities[particle,var] = velocities[nears[particle],var]
                
        return velocities
        
    def __craziness(self,velocities):
 
        for particle in range(self.num_particles):
            
            crazinessBird = np.random.rand()
            
            if crazinessBird < 0.02:
                
                newVel = np.random.randn(1,self.num_vars)*0.03
                for var in range(self.num_vars):
                    velocities[particle,var] = newVel[0,var]
                
        return velocities
    
    def __roost(self,particles,objective):
        
        gbestVal = np.inf
        gbest = 1;
         
        for particle in range(self.num_particles):                   #Para cada passaro do bando.
            #Calcula a distancia euclidiana para a posicao da comida.
            dist = self.__distEuclidean(particles[particle], objective)
            if gbestVal > dist:        #Se e menor que a ja existente
                gbest = particle;          #Substitui.
                gbestVal = dist;
         
        return gbest,gbestVal       
    
    def __cornfieldVector(self,particles, velocities, gbest):
 
        # Alternar entre valores: 0.006 0.01 0.02 0.0001
        INCREMENT = 0.01;
        LIMIT = 0.07;
         
        for particle in range(self.num_particles):
            for var in range(self.num_vars):
                if(particles[particle,var] > particles[gbest,var]) and (velocities[particle,var] > -LIMIT):
                    velocities[particle,var] = velocities[particle,var] - (np.random.rand()*INCREMENT)    
                elif (particles[particle,var] < particles[gbest,var]) and (velocities[particle,var] < LIMIT):
                    velocities[particle,var] = velocities[particle,var] + (np.random.rand()*INCREMENT)    
        return velocities
    
    def search(self,target,max_error):
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.ion() 
        
        #Geracao da matriz de passaros, cada passaro e um conjunto 3D de pontos.
        #Inicialmente a posicao e aleatoria.
        particles = np.random.randn(self.num_particles,self.num_vars)*3
     
        #Geracao do vetor de movimento de cada passaro. Inicialmente aleatorio.
        velocities = np.random.randn(self.num_particles,self.num_vars)*0.03
     
        #Armezena o melhor valor ao logo de cada iteracao
        #gbestVal = np.zeros(self.max_num_interactions)
        gbestValHist = []
    
        #Executa o voo.
        interaction=0
                
        while interaction < self.max_num_interactions:
        
            #Encontra o passaro que tem amenor distancia para a comida
            gbest,gbestVal = self.__roost(particles, target)
            gbestValHist.append(gbestVal)
            
            if self.option == 1:
                #Calcula a nova velocidade dos passaros pelo metodo
                #Nearest Neighbor Velocity Matching.
                velocities=self.__velocityMatching(particles, velocities)
                #Introduz a variavel Craziness.
                self.velocities=self.__craziness(velocities)
            
            if self.option == 2:
                #Recalcula a velocidade baseada no passaro de maior sucesso.
                velocities = self.__cornfieldVector(particles, velocities, gbest)
        
            #Recalcula a posicao de cada passaro.
            particles = particles+velocities
            
            plt.cla()
            ax.scatter(target[0], target[1], target[2], s=80, c='b', marker='x')
            ax.scatter(particles[:,0], particles[:,1], particles[:,2], c='r', marker='o')
            plt.pause(0.0001)
            
            #Muda a posicao da comida.
            if gbestVal <= max_error:
                #Descomente o "break" caso queira finalizar o algoritmo 
                #ao achar a solução                 
                #break; 
                target = np.random.randn(self.num_vars)*5;
            interaction = interaction+1            
        
        plt.clf()    
        return gbestValHist
    
#     def __printParticles(self,ax,particles):
        
        