import os, sys; sys.path.insert(0, os.environ['WORKDIR'])
import pandas as pd
from collections import deque

import subprocess
from itertools import product
from time import sleep
from torch import cuda

CHANNELs = ["Skim1E2Mu", "Skim3Mu"]
SIGNALs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
           "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
           "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
           "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
BACKGROUNDs = ["TTLL_powheg", "ttX"]
MODELs = ["ParticleNet", "ParticleNetLite"]
OPTIMIZERs = ["RMSprop", "Adadelta", "Adam", "AdamW"]
INITLRs = [0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005,
           0.001, 0.002, 0.005, 0.01, 0.02, 0.05]
SCHEDULERs = ["StepLR", "ExponentialLR", "CyclicLR"]

def assertParameters(channel, signal, background, model, optim, initLR, scheduler):
    try:
        assert channel in CHANNELs
        assert signal in SIGNALs
        assert background in BACKGROUNDs
        assert model in MODELs
        assert optim in OPTIMIZERs
        assert initLR in INITLRs
        assert scheduler in SCHEDULERs
    except Exception as e:
        print(e)
        exit(1)

def addJobCommands(queue):
    csv = pd.read_csv("MetaInfo/modelInfo.csv", sep=",\s", comment="#", engine="python")
    for idx in csv.index:
        channel = csv.loc[idx, 'channel']
        sig, bkg = csv.loc[idx, 'signal'], csv.loc[idx, 'background']
        model = csv.loc[idx, 'model']
        optim = csv.loc[idx, 'optimizer']
        initLR = csv.loc[idx, 'initLR']
        scheduler = csv.loc[idx, 'scheduler']
        assertParameters(channel, sig, bkg, model, optim, initLR, scheduler)

        command = "python triLepRegion/trainModels.py"
        command += f" --signal {sig}"
        command += f" --background {bkg}"
        command += f" --channel {channel}"
        command += f" --model {model}"
        command += f" --optimizer {optim}"
        command += f" --initLR {initLR}"
        command += f" --scheduler {scheduler}"
        queue.append(command)

def checkDeviceStatus(device, procs, freeMemory=2e9, maxRunningJobs=12):
    runningJobs = list(filter(lambda proc: proc.poll() is None, procs))
    free, max = cuda.mem_get_info(device)
    return (free > freeMemory) and (len(runningJobs) < maxRunningJobs)

if __name__ == "__main__":
    multiProcs = {}
    for i in range(cuda.device_count()):
        device = f"cuda:{i}"
        multiProcs[device] = []

    queue = deque()
    addJobCommands(queue)

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

