# In this script, the codes for hyperparameter optimization using genetic algorithm
# is summarized. The method for selection, crossover, and mutation is from
# https://link.springer.com/content/pdf/10.1007/s11042-020-10139-6.pdf
import os
import sys; sys.path.insert(0, os.environ['WORKDIR'])
import random
import numpy as np
import pandas as pd
from itertools import product


class GeneticModule():
    def __init__(self):
        self.hyperSet = []
        self.population = None
    
    def getGeneValues(self, genes):
        self.hyperSet.append(genes)
        
    def generatePool(self, criteria=None):
        self.pool = list(product(*self.hyperSet))
        if not criteria is None:
            self.pool = list(filter(criteria, self.pool))
        
    def randomGeneration(self, nPop=10):
        population = {}
        for idx, chromosome in enumerate(random.choices(self.pool, k=nPop)):
            population[idx] = {"chromosome": chromosome,
                               "fitness": None}
        self.population = population
        
    def updatePopulation(self, masspoint, background, channel):
        # get hyperparams
        for idx in range(len(self.population)):
            model, optimizer, initLR, scheduler = self.population[idx]['chromosome']
            path = f"{os.environ['WORKDIR']}/triLepRegion/full/{channel}__/{masspoint}_vs_{background}/plots/training-{model}_{optimizer}_initLR-{str(initLR).replace('.', 'p')}_{scheduler}.csv"
            csv = pd.read_csv(path)
            train_loss = float(csv.sort_values('loss/valid').iloc[0].loc['loss/train'])
            valid_loss = float(csv.sort_values('loss/valid').iloc[0].loc['loss/valid'])
            panelty = 1.5*abs(train_loss - valid_loss)
            # fitness as the harmonic mean of valid loss and panelty
            #fitness = 2*valid_loss*panelty/(valid_loss+panelty)
            fitness = valid_loss + panelty # valid_loss + overtraining panelty
            self.population[idx]['fitness'] = fitness
    
    def __getIdxFromRoulette(self, nPop):
        probs = np.array(range(nPop+1))
        roulette = np.cumsum(probs)
        dart = sum(probs) * np.random.rand()
        idx = np.argwhere(dart <= roulette)[0][0]-1
        return idx
    
    def rankSelection(self):
        while True:
            idx1 = self.__getIdxFromRoulette(len(self.population))
            idx2 = self.__getIdxFromRoulette(len(self.population))
            parent1 = sorted(self.population.values(), key=lambda x: x['fitness'], reverse=True)[idx1]
            parent2 = sorted(self.population.values(), key=lambda x: x['fitness'], reverse=True)[idx2]
    
            if parent1['fitness'] == parent2['fitness']:
                continue
            else:
                break
        return (parent1, parent2)
        
    def uniformCrossOver(self, parent1, parent2):
        child = {}
        while True:
            chromosome = []
            for i in range(len(parent1['chromosome'])):
                # throw coin
                if np.random.rand() > 0.5:
                    chromosome.append(parent1['chromosome'][i])
                else:
                    chromosome.append(parent2['chromosome'][i])
            chromosome = tuple(chromosome)
            if chromosome in self.pool:
                child['chromosome'] = chromosome
                break
            else:
                continue
        return child
    
    def displacementMutation(self, child, thresholds):
        mutation = {}
        while True:
            chromosome = []
            for i in range(len(child['chromosome'])):
                # throw coin
                if np.random.rand() > thresholds[i]:
                    chromosome.append(random.choice(self.hyperSet[i]))
                else:
                    chromosome.append(child['chromosome'][i])
        
            chromosome = tuple(chromosome)
            if chromosome in self.pool:
                mutation['chromosome'] = chromosome
                mutation['fitness'] = None
                break
            else:
                continue
        return mutation
    
    def evolution(self, thresholds, ratio):
        parents = sorted(self.population.values(), key=lambda x: x['fitness'], reverse=True)
        children = []
        nPop = len(self.population)
        nbirth = int(len(self.population)*ratio)
        for _ in range(nbirth):
            temp_population = []
            for gene in parents+children:
                temp_population.append(gene['chromosome'])
            while True:
                p1, p2 = self.rankSelection()
                child = self.uniformCrossOver(p1, p2)
                mutation = self.displacementMutation(child, thresholds)  
                # don't allow the same mutation
                # with parents or already produced mutation
                if mutation['chromosome'] in temp_population:
                    continue
                children.append(mutation) 
                break

        self.population = {}
        for idx in range(nbirth):
            self.population[idx] = children[idx]
            # delete bad parents from pool
            if parents[idx]['chromosome'] in self.pool:
                self.pool.remove(parents[idx]['chromosome'])

        for idx in range(nbirth, nPop):
            self.population[idx] = parents[idx]

        del parents, children
        
    def meanFitness(self):
        fitness = []
        for idx in range(len(self.population)):
            this_fitness = self.population[idx]['fitness']
            if this_fitness is None:
                continue
            fitness.append(this_fitness)
        return np.mean(fitness)

    def savePopulation(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        df = pd.DataFrame(self.population)
        df.to_csv(path, index_label=False)        
        
