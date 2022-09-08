import os
import subprocess
from itertools import product

MASSPOINTs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
              "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
              "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
              "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
BACKGROUNDs = ["TTLL_powheg", "VV"]

#### hyperparameters
optimizer = "Adam"
schedulers = ["ExponentialLR"]
initial_lrs = [1e-3, 2e-3, 5e-3, 1e-2, 5e-2]
batch_size = 1024
hidden_layer = 128

for mp, bkg in product(MASSPOINTs, BACKGROUNDs):
    procs = []
    for scheduler, initial_lr in product(schedulers, initial_lrs):
        command = f"python trainModels.py --signal {mp} --background {bkg} --batch_size {batch_size} --optimizer {optimizer} --initial_lr {initial_lr} --scheduler {scheduler} --hidden_layers {hidden_layer}"
        proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        procs.append(proc)

    for proc in procs:
        proc.communicate()
        assert proc.returncode == 0
