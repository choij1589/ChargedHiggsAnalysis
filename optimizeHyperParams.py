import os
import sys
from threading import currentThread; sys.path.insert(0, os.environ['WORKDIR'])
import subprocess
import torch 

from collections import deque
from time import sleep
from pprint import pprint

from libPython.GATools import GeneticModule

MASSPOINT = "MHc-130_MA-90"
BACKGROUND = "TTLL_powheg"

# Let's run the model linearly first
#### Hyper parameters
models = ["ParticleNet"]
optimizers = ["RMSprop", "Adam", "AdamW", "Adadelta"]
schedulers = ["StepLR", "ExponentialLR", "CyclicLR"]
initLRs = [0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 
           0.001, 0.002, 0.005, 0.01, 0.02, 0.05]
nBatch = 1024
nHidden = 128
criteria = lambda x: "RMSprop" in x or "CyclicLR" not in x
nPop = 6
thresholds = [0.7, 0.7, 0.9, 0.7]

def evalFitness(population):
    procs = []
    for idx in range(nPop):
        # already estimated
        if population[idx]['fitness'] is not None:
            continue
        model, optimizer, initLR, scheduler = population[idx]['chromosome']
        command = f"python triLepRegion/trainModels.py --signal {MASSPOINT} --background {BACKGROUND}"
        command += f" --model {model}"
        command += f" --optimizer {optimizer}"
        command += f" --initLR {initLR}"
        command += f" --scheduler {scheduler}"
        command += f" --device cuda --pilot"
        #print(f"sumbit {command}...")
        proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        procs.append(proc)
        
    for proc in procs:
        proc.communicate()
        assert proc.returncode == 0


# generate pool
gaModule = GeneticModule()
gaModule.getGeneValues(models)
gaModule.getGeneValues(optimizers)
gaModule.getGeneValues(initLRs)
gaModule.getGeneValues(schedulers)
gaModule.generatePool(criteria)

maxIter = 3
gaModule.randomGeneration(nPop=nPop)
for iter in range(maxIter):
    print(f"@@@@ generation {iter}")
    evalFitness(gaModule.population)
    gaModule.updatePopulation(MASSPOINT, BACKGROUND)
    gaModule.evolution(thresholds=thresholds, ratio=0.5)
    print(gaModule.meanFitness())
    
path = f"{os.environ['WORKDIR']}/models/{MASSPOINT}_vs_{BACKGROUND}/GAOptimization.csv"
gaModule.savePopulation(path=path)