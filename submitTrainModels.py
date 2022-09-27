import subprocess
from itertools import product
from collections import deque
from time import sleep
from torch import cuda

MASSPOINTs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
              "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
              "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
              "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
BACKGROUNDs = ["TTLL_powheg", "VV"]

#### hyperparameters
models = ["GCN", "GNN", "ParticleNet"]
optimizers = ["RMSprop", "Adam"]
schedulers = ["StepLR", "ExponentialLR"]
initLRs = [0.0001, 0.0005, 0.001, 0.002, 0.005]
nBatch = 1024
nHidden = 128

def makeJobCommands():
    job_list = product(MASSPOINTs, BACKGROUNDs, optimizers, schedulers, initLRs)
    queue = deque()
    for sig, bkg, optim, scheduler, initLR in job_list:
        command = f"python triLepRegion/trainModels.py --signal {sig} --background {bkg} --batch_size {nBatch} --optimizer {optim} --scheduler {scheduler} --initial_lr {initLR} --hidden_layers {nHidden}"
        queue.append(command)
    return queue

def checkDeviceStatus(device, procs, freeMemory=2e9, maxRunningJobs=14):
    runningJobs = list(filter(lambda proc: proc.poll() is None, procs))
    free, max = cuda.mem_get_info(device)
    return (free > freeMemory) and (len(runningJobs) < maxRunningJobs)

# device number gpus
multiProcs = {}
for i in range(cuda.device_count()):
    device = f"cuda:{i}"
    multiProcs[device] = []

queue = makeJobCommands()
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
