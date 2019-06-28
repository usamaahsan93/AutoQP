
from copy import deepcopy
import numpy as np
from numpy.random import choice, random as rand, randint

from QGates import gateArity
import os
import pickle as pkl


class kueGP:
    
    def __init__(self,population, qBits,maxIndividualSize,fitnessFn,
                 eliteUnit=1,mutationRate=0.5,maxIndividualSizeProbability=0.8,
                 crossoverRate=0.7, generations=1, stoppingCriteria=0.9999):
        '''
        population: Population of genetic programming (int)
        
        qBits : Qubits used for the quantum code (int)
        
        maxIndividualSize: Maximum size/length of the individual (int)
        
        eliteUnit: Elite individuals in population to be selected as it is for        
        the next generation. This should be less than the population
        
        mutationRate: Mutation Rate (genetic programming parameter) (0 to 1) (float)
        
        maxIndividualSizeProbability: Individuals to reach max length (only used
        to initialize the population) (0 to 1) (float)
        
        crossoverRate:Crossover Rate (genetic programming parameter) (0 to 1) (float)
        
        generations: Generations (genetic programming parameter) (int)
        
        stoppingCriteria: max fitness desired by the user (not yet clearly defined
        right now, its better to leave it as it is right now) (0~1) (float)
        
        fitnessFn: Fitness function required to score the individual. This has
        to be written by the user. Fitness function should be designed in such
        a way that it is able to take the list of tuples containing a keyword ORACLE
        and returns the fitness score between 0 to 1.
        '''      
        
        self.population=population
        self.operand=range(qBits)
        self.operator=list(gateArity.keys())
        self.maxIndividualSize=maxIndividualSize
        self.eliteUnit=eliteUnit
        self.mutationRate=mutationRate
        self.maxIndividualSizeProbability=maxIndividualSizeProbability
        self.crossoverRate=crossoverRate
        self.generations=generations
        self.__generationFitness=0
        self.fitnessFn=fitnessFn
        self.stoppingCriteria=stoppingCriteria
        
        self.txtName='./'+'p'+str(population)+'_mR'+str(mutationRate)+'_cR'+str(crossoverRate)+'_g'+str(generations)
#        self.txtName='./BernsteinVazirani_p1000_g50_mR0.5_cR_0.7'
        self.fileName=self.txtName+'.pkl'
        p=os.path.isfile(self.fileName)

        if p:
            print('LOADING FROM SAVED FILE [FILE NAME] : ',self.fileName)
            with open(self.fileName,'rb') as file:
                self.populationSet=pkl.load(file)
            file.close()
            
        else:
            print('LOADING NULL POPULATION...')
            self.populationSet=[]
            
            
##################################################### 
    
    def __singleGene(self):
        '''
        This function generates the single individual of genetic program
        '''
        
        count=0
        
        l=[]
        while(1):
            if count>=self.maxIndividualSize:
                break;
            else:
                tpl=self.__tupleConstruct()
                    
                l.append(tpl)
                
                if rand()<self.maxIndividualSizeProbability:
                    
                    count+=1
                    
                else:
                    break       

        idx=randint(0,len(l))
        l.insert(idx,'ORACLE')
        
        return l
    
##################################################### 

    def __populationGeneration(self):
        '''
        This function generates the population
        '''
        
        for i in range(self.population):
            self.populationSet.append(self.__singleGene())
              
##################################################### 

    def __tupleConstruct(self):
        '''
        This function generates the tuple (gene) of the genetic programming
        chromosomes. Which are later appended in a list to form an individual
        '''
        
        #Select an operator i.e. quantum gate
        optr=choice(self.operator)
        
        #if chosen gate has arity of 2 then select two different qubits and form a tuple
        if gateArity.get(optr)==2:
            i,j=1,1
            while(i==j):
                i=choice(self.operand)
                j=choice(self.operand)
            
            tpl=(optr,i,j)
        
        else:
            tpl=(optr,choice(self.operand))
            
        return tpl

#####################################################
    def __fitnessPopulation(self):
        '''
        This function passes the whole population through a fitness function
        one by one and append their scores in a list and when whole population
        is done it returns it score.
        '''
        
        score=[]
        for i in self.populationSet:
            currentFitness=self.fitnessFn(i)
            score.append(currentFitness)
            self.__generationFitness=np.mean(score)

        return score
                
##################################################### 


    def fit(self):
        '''
        This function executes the genetic programming algorithm. It does the
        population generation,fitness evaluation, selection, crossover, mutation
        and returns the 1 optimal individual out of many along with the max fitness
        score along the generations.

        '''
        
        #Check for elite unit which should be less than the population
        if self.population<=self.eliteUnit:
            print('ERROR: Elite Selection is greater than population')
            return
        
        #Displaying the summary
        print('Running on the following Configurations:\n\n'\
              'Population Backup File Name\t:\t',self.fileName,'\n'\
              'Population\t:\t',self.population,'\n'\
              'Elite Units\t:\t',self.eliteUnit,'\n'\
              'Generation\t:\t',self.generations,'\n'\
              'Stopping Criteria:\t',self.stoppingCriteria,'\n')
        

        selectedPopulation=[]
        print('\nGENERATION\t\tGENERATION AVERAGE FITNESS\t\tBEST UNIT\'s FITNESS')
        print('___________\t\t__________________________\t\t___________________\n')
        gen=1
        
        #Generating Population
        self.__populationGeneration()
      
        allfitness=[]
        allOptimal=[]
        #Check to exit when whole generation completed
        while(gen<=self.generations):
            pop=0
            #Fitness of whole population is returned in x
            x=self.__fitnessPopulation()
            
            #Optimal fitness of the current generation is taken 
            optimal=self.populationSet[np.argmax(x)]
            allfitness.append(max(x))
            
            #Writing on file selected individual along with its fitness
            with open(self.txtName+'.txt','a') as f:
                f.write(str(optimal)+' Fitness : '+str(max(x))+'\n')                
                f.close()
            
            #It writes in the file all the optimal individuals in the current generation
            if np.max(x)>=self.stoppingCriteria:                
                for i in range(len(x)):
                    if x[i] == np.max(x):
                        if self.populationSet[i] not in allOptimal:
                            allOptimal.append(optimal)
                            with open(self.txtName+'_AllOptimal_'+'.txt','a') as f:
                                f.write(str(self.populationSet[i])+'\n')                
                                f.close()
            
            #Forming variable p which is setting the selection probabilities according the fitness of individual
            F=np.asarray(x)         
            idx=np.argsort(F)
            p=np.cumsum(F[idx])/(np.sum(F)+1e-10)
            
            #Copying elite individuals
            for i in range(self.eliteUnit):
                selectedPopulation.append(self.populationSet[idx[(i+1)*-1]])
            

            print('{}\t\t\t{}\t\t\t{}'.format(gen,self.__generationFitness,np.max(x)))
            
            #Updating the population by applying selection, crossover and mutation
            while pop<self.population:
                code=deepcopy(self.__selection(p,idx))
                
                if rand()<self.mutationRate:
                    mCode=self.__mutation(code)
                    selectedPopulation.append(mCode)
                    pop+=1
                    
                if rand()<self.crossoverRate:
                    code2=deepcopy(self.__selection(p,idx))
                    
                    p1,p2=self.__crossover(code,code2)
                    selectedPopulation.append(p1)
                    selectedPopulation.append(p2)                   
                    pop+=2
                
                else:
                    selectedPopulation.append(code)
                    pop+=1

            if len(selectedPopulation)>self.population:
                selectedPopulation=selectedPopulation[:-1]
            
            self.populationSet=deepcopy(selectedPopulation)
            gen+=1
            
            #Saving the current population to make this 
            with open(self.fileName,'wb') as file:
                pkl.dump(self.populationSet,file)
            file.close()

        return allOptimal, allfitness
#######################################################################
        
     
    def __substringORACLE(self,x):
        '''
        It takes the individual and return two substring which are created
        by taking ORACLE keyword as a pivot
        
        INPUT:Individual of genetic program
        OUTPUT: Individual broken into two substring at the keyword ORACLE
        '''
        
        idx=x.index('ORACLE')
        str1=x[0:idx]
        str2=x[idx+1:]
        
        return str1,str2
    
    
#######################################################################

    def __crossover(self,p1,p2):
        '''
         This function is the genetic programming module used for the crossover
        in the two selected individual. Substrings from both of the individuals
        is swapped between them.
        
        INPUT: Two individuals
        OUTPUT: Crossover between the individuals
        '''
        
        #Generating two substrings from both individuals one is before ORACLE keyword and one from after
        p1a,p1b=self.__substringORACLE(p1)
        p2a,p2b=self.__substringORACLE(p2)
        
        #Check is placed that if crossover substring is greater than 0 only then perform the crossover
        if len(p1a)>0 and len(p2a)>0:
            idxp1a=randint(0,len(p1a))
            idxp2a=randint(0,len(p2a))
            p1a[idxp1a:],p2a[idxp2a:]=p2a[idxp2a:],p1a[idxp1a:]
            
        if len(p1b)>0 and len(p2b)>0 :
            idxp1b=randint(0,len(p1b))            
            idxp2b=randint(0,len(p2b))
            p1b[idxp1b:],p2b[idxp2b:]=p2b[idxp2b:],p1b[idxp1b:]

            p1a.append('ORACLE')
            p1a.extend(p1b)
        
            p2a.append('ORACLE')
            p2a.extend(p2b)
        
            p1=p1a
            p2=p2a
        
        return p1,p2



###########################################################
            
    def __mutation(self,code):
        '''
        This function is the genetic programming module used for the mutation
        in the selected individual. It performs 1 mutation out of 3 types randomly.
        
        Mutation Types:
        INSERT a tuple
        DELETE a tuple
        SWAP between two tuples
        
        INPUT: Genetic programming individual
        OUTPUT: Mutated individual
        '''
        
        #Selecting mutation position in an individual randomly      
        tplIdx=randint(0,len(code))
        
        #Selecting type of mutation randomly
        mType=randint(0,2)

        if mType==0:
            tpl=self.__tupleConstruct()
            code.insert(tplIdx,tpl)           
            
        elif mType==1 and len(code)>1 and code[tplIdx]!='ORACLE':
            del code[tplIdx]
                
        elif mType==2:
            while(1):
                tplIdx2=randint(0,len(code)-1)
                if tplIdx==tplIdx2:
                    continue
                else:
                    break
                
            code[tplIdx],code[tplIdx2]=code[tplIdx2],code[tplIdx]
            
        return code


##################################################### 
          
            
    def __selection(self,p,idx):
        '''
        This function does the selection of the individual. It selects the
        individual based on two strategies, i.e. random selection and roulette
        wheel selection
        
        INPUT: 
            p: probability string giving the uneven selection space to individuals
            idx: sorted index according to probability
        '''
        
        if rand()<0.5:
            findIdx=randint(0,self.population)
            return self.populationSet[findIdx]
        
        else:
            findIdx=(np.where ((rand()<p) ==True))[0][0]
            return self.populationSet[idx[findIdx]]            

####################################################        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
            