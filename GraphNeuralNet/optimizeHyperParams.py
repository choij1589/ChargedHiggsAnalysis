import os
import argparse
import subprocess

from time import sleep
from libPython.GATools import GeneticModule

parser = argparse.ArgumentParser()
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--background", required=True, type=str, help="background")
parser.add_argument("--channel", required=True, type=str, help="channel")
args = parser.parse_args()

WORKDIR = os.environ['WORKDIR']
modelPath = f"{WORKDIR}/GraphNeuralNet/{args.channel}/{args.signal}_vs_{args.background}/models"
os.makedirs(modelPath)
os.makedirs(modelPath.replace("models", "CSV"))

# Let's run the model linearly first
#### Hyper parameters
nNodes = [32, 64, 128]
#optimizers = ["RMSprop", "Adam", "AdamW", "Adadelta"]
optimizers = ["RMSprop", "Adam", "NAdam", "RAdam"]
schedulers = ["StepLR", "CyclicLR"]
#initLRs = [0.001, 0.002, 0.005, 0.008, 0.01]
initLRs = [0.0001, 0.0005, 0.001, 0.002, 0.01]
nBatch = 1024
# criteria = lambda x: "RMSprop" in x or "CyclicLR" not in x
nPop = 14
thresholds = [0.5, 0.5, 0.5, 0.5]
maxIter = 5

def evalFitness(population):
    procs = []
    for idx in range(nPop):
        # already estimated
        if population[idx]['fitness'] is not None:
            continue
        nNodes, optimizer, initLR, scheduler = population[idx]['chromosome']
        command = f"python {WORKDIR}/GraphNeuralNet/trainModel.py --signal {args.signal} --background {args.background}"
        command += f" --channel {args.channel}"
        command += f" --model ParticleNet"
        command += f" --nNodes {nNodes}"
        command += f" --optimizer {optimizer}"
        command += f" --initLR {initLR}"
        command += f" --scheduler {scheduler}"
        command += f" --device cuda"
        print(f"sumbit {command}...")
        proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        procs.append(proc)
        sleep(1)
        
    for proc in procs:
        proc.communicate()
        assert proc.returncode == 0


# generate pool
gaModule = GeneticModule()
gaModule.getGeneValues(nNodes)
gaModule.getGeneValues(optimizers)
gaModule.getGeneValues(initLRs)
gaModule.getGeneValues(schedulers)
gaModule.generatePool()

gaModule.randomGeneration(nPop=nPop)
evalFitness(gaModule.population)
gaModule.updatePopulation("GraphNeuralNet", args.signal, args.background, args.channel)
print("@@@@ generation 0")
print(f"@@@@ mean fitness: {gaModule.meanFitness()}")
path = f"{WORKDIR}/GraphNeuralNet/{args.channel}/{args.signal}_vs_{args.background}/CSV/GAOptimGen0.csv"
gaModule.savePopulation(path=path)
for iter in range(1, maxIter):
    print(f"@@@@ generation {iter}")
    gaModule.evolution(thresholds=thresholds, ratio=0.5)
    evalFitness(gaModule.population)
    gaModule.updatePopulation("GraphNeuralNet", args.signal, args.background, args.channel)
    print(f"@@@@ mean fitness: {gaModule.meanFitness()}")
    path = f"{WORKDIR}/GraphNeuralNet/{args.channel}/{args.signal}_vs_{args.background}/CSV/GAOptimGen{iter}.csv"
    gaModule.savePopulation(path=path)
