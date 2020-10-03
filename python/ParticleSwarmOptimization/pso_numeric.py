"""
Adaptado de: 
@author: edielson - https://github.com/edielsonpf
"""

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
    
    def __Rosenbrock(self,particle):
        x1=particle[0]
        x2=particle[1]
        return (1-x1)**2+100.0*(x2-x1**2)**2
    
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
            #dist = self.__distEuclidean(particles[particle], objective)
            dist = self.__Rosenbrock(particles[particle])            
            if gbestVal > dist:        #Se e menor que a ja existente
                gbest = particle;          #Substitui.
                gbestVal = dist;                
         
        return gbest,gbestVal       
    
    def __cornfieldVector(self,particles, velocities, gbest):
 
        # Alternar entre valores: 0.01, 0.007, 0.005, 0.003, 0.001
        INCREMENT = 0.0001;
        LIMIT = 0.07;
         
        for particle in range(self.num_particles):
            for var in range(self.num_vars):
                if(particles[particle,var] > particles[gbest,var]) and (velocities[particle,var] > -LIMIT):
                    velocities[particle,var] = velocities[particle,var] - (np.random.rand()*INCREMENT)    
                elif (particles[particle,var] < particles[gbest,var]) and (velocities[particle,var] < LIMIT):
                    velocities[particle,var] = velocities[particle,var] + (np.random.rand()*INCREMENT)    
        return velocities
    
    def search(self,target,max_error):
        
        #Geracao da matriz de passaros, cada passaro e um conjunto 3D de pontos.
        #Inicialmente a posicao e aleatoria.
        particles = np.random.uniform(-1,1,(self.num_particles,self.num_vars))
        
        #Geracao do vetor de movimento de cada passaro. Inicialmente aleatorio.
        velocities = np.random.randn(self.num_particles,self.num_vars)*0.03
     
        #Armezena o melhor valor ao logo de cada iteracao
        #gbestVal = np.zeros(self.max_num_interactions)
        gbestValHist = []
    
        #Executa o voo.
        interaction=0
        
        #Encontra o passaro que tem amenor distancia para a comida
        gbest,gbestVal = self.__roost(particles, target)
        
        gbestValHist.append(gbestVal)
                        
        while (interaction < self.max_num_interactions) and (np.abs(gbestVal-target) > max_error):
        
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
            
            #Encontra o passaro que tem amenor distancia para a comida
            gbest,gbestVal = self.__roost(particles, target)
            
            gbestValHist.append(gbestVal)
                        
            interaction = interaction+1

        return gbestValHist,particles[gbest],gbestVal
           
        