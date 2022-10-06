import os, sys; sys.path.insert(0, os.environ['WORKDIR'])
import pandas as pd
from collections import deque

import subprocess
from itertools import product
from time import sleep
from torch import cuda

#SIGNALs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
#           "MHc-100_MA-60", "MHc-100_MA-95",
#           "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
#           "MHc-160_MA-85", "MHc-160_MA-155"]
SIGNALs = ["MHc-70_MA-15", "MHc-100_MA-60", "MHc-130_MA-90", "MHc-160_MA-155"]
#BACKGROUNDs = ["TTLL_powheg"]
BACKGROUNDs = ["VV"]

def makePopulation(sig, bkg):
    path = f"{os.environ['WORKDIR']}/models/pilot/{sig}_vs_{bkg}/GAOptimization.csv"
    csv = pd.read_csv(path).T
    
    population = []
    for idx in csv.index:
        chromosome = csv.loc[idx, 'chromosome'][1:-1].split(", ")
        model = chromosome[0][1:-1]
        optim = chromosome[1][1:-1]
        initLR = float(chromosome[2])
        scheduler = chromosome[3][1:-1]
        population.append((model, optim, initLR, scheduler))
    population = list(set(population))
    return population

def addJobCommands(queue, sig, bkg):
    job_list = makePopulation(sig, bkg)
    for model, optim, initLR, scheduler in job_list:
        command = f"python triLepRegion/trainModels.py"
        command += f" --signal {sig}"
        command += f" --background {bkg}"
        command += f" --model {model}"
        command += f" --optimizer {optim}"
        command += f" --initLR {initLR}"
        command += f" --scheduler {scheduler}"
        queue.append(command)

def checkDeviceStatus(device, procs, freeMemory=2e9, maxRunningJobs=14):
    runningJobs = list(filter(lambda proc: proc.poll() is None, procs))
    free, max = cuda.mem_get_info(device)
    return (free > freeMemory) and (len(runningJobs) < maxRunningJobs)

if __name__ == "__main__":
    multiProcs = {}
    for i in range(cuda.device_count()):
        device = f"cuda:{i}"
        multiProcs[device] = []

    queue = deque()
    for sig, bkg in product(SIGNALs, BACKGROUNDs):    
        addJobCommands(queue, sig, bkg)
    
    # submit all jobs till the queue empty
    while queue:
        for device, procs in multiProcs.items():
            if checkDeviceStatus(device, procs):
                command = f"{queue.popleft()} --device {device}"
                print(f"submit {command}...")
                proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                procs.append(proc)
            sleep(1)
    
    # check all jobs are done
    for procs in multiProcs.values():
        for proc in procs:
            proc.communicate()
            assert proc.returncode == 0
