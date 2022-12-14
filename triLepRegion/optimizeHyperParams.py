import os
import sys; sys.path.insert(0, os.environ['WORKDIR'])
import argparse
import subprocess

from time import sleep
from libPython.GATools import GeneticModule

parser = argparse.ArgumentParser()
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--background", required=True, type=str, help="background")
parser.add_argument("--channel", required=True, type=str, help="channel")
args = parser.parse_args()

model_path = f"{os.environ['WORKDIR']}/triLepRegion/full/{args.channel}__/{args.signal}_vs_{args.background}/models"
os.makedirs(model_path)

# Let's run the model linearly first
#### Hyper parameters
models = ["ParticleNet", "ParticleNetLite"]
optimizers = ["RMSprop", "Adam", "AdamW", "Adadelta"]
schedulers = ["StepLR", "CyclicLR"]
initLRs = [0.0001, 0.0002, 0.0005, 
           0.001, 0.002, 0.005, 
           0.01, 0.02, 0.05]
nBatch = 1024
# criteria = lambda x: "RMSprop" in x or "CyclicLR" not in x
nPop = 12
thresholds = [0.7, 0.7, 0.7, 0.7]
maxIter = 4

def evalFitness(population):
    procs = []
    for idx in range(nPop):
        # already estimated
        if population[idx]['fitness'] is not None:
            continue
        model, optimizer, initLR, scheduler = population[idx]['chromosome']
        command = f"python {os.environ['WORKDIR']}/triLepRegion/trainModels.py --signal {args.signal} --background {args.background}"
        command += f" --channel {args.channel}"
        command += f" --model {model}"
        command += f" --optimizer {optimizer}"
        command += f" --initLR {initLR}"
        command += f" --scheduler {scheduler}"
        command += f" --device cuda"
        #command += f" --device cuda --pilot"
        print(f"sumbit {command}...")
        proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        procs.append(proc)
        sleep(1)
        
    for proc in procs:
        proc.communicate()
        assert proc.returncode == 0


# generate pool
gaModule = GeneticModule()
gaModule.getGeneValues(models)
gaModule.getGeneValues(optimizers)
gaModule.getGeneValues(initLRs)
gaModule.getGeneValues(schedulers)
gaModule.generatePool()

gaModule.randomGeneration(nPop=nPop)
evalFitness(gaModule.population)
gaModule.updatePopulation(args.signal, args.background, args.channel)
print("@@@@ generation 0")
print(f"@@@@ mean fitness: {gaModule.meanFitness()}")
path = f"{os.environ['WORKDIR']}/triLepRegion/full/{args.channel}__/{args.signal}_vs_{args.background}/models/GAOptimization_gen0.csv"
gaModule.savePopulation(path=path)
for iter in range(1, maxIter):
    print(f"@@@@ generation {iter}")
    gaModule.evolution(thresholds=thresholds, ratio=0.5)
    evalFitness(gaModule.population)
    gaModule.updatePopulation(args.signal, args.background, args.channel)
    print(f"@@@@ mean fitness: {gaModule.meanFitness()}")
    path = f"{os.environ['WORKDIR']}/triLepRegion/full/{args.channel}__/{args.signal}_vs_{args.background}/models/GAOptimization_gen{iter}.csv"
    gaModule.savePopulation(path=path)
