import os
import sys; sys.path.insert(0, os.environ['WORKDIR'])
import argparse
import subprocess

from libPython.GATools import GeneticModule

parser = argparse.ArgumentParser()
parser.add_argument("--signal", "-s", required=True, type=str, help="signal mass point")
parser.add_argument("--background", "-b", required=True, type=str, help="background")
args = parser.parse_args()

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
thresholds = [0.7, 0.8, 0.95, 0.8]
maxIter = 5

def evalFitness(population):
    procs = []
    for idx in range(nPop):
        # already estimated
        if population[idx]['fitness'] is not None:
            continue
        model, optimizer, initLR, scheduler = population[idx]['chromosome']
        command = f"python {os.environ['WORKDIR']}/triLepRegion/trainModels.py --signal {args.signal} --background {args.background}"
        command += f" --model {model}"
        command += f" --optimizer {optimizer}"
        command += f" --initLR {initLR}"
        command += f" --scheduler {scheduler}"
        command += f" --device cuda --pilot"
        print(f"sumbit {command}...")
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

gaModule.randomGeneration(nPop=nPop)
evalFitness(gaModule.population)
gaModule.updatePopulation(args.signal, args.background)
print("@@@@ generation 0")
print(f"@@@@ mean fitness: {gaModule.meanFitness()}")
for iter in range(1, maxIter):
    print(f"@@@@ generation {iter}")
    gaModule.evolution(thresholds=thresholds, ratio=0.5)
    evalFitness(gaModule.population)
    gaModule.updatePopulation(args.signal, args.background)
    print(f"@@@@ mean fitness: {gaModule.meanFitness()}")
    
path = f"{os.environ['WORKDIR']}/models/{args.signal}_vs_{args.background}/GAOptimization.csv"
gaModule.savePopulation(path=path)
