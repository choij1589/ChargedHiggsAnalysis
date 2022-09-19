import os
import subprocess

MASSPOINTs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
              "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
              "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
              "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
BACKGROUNDs = ["TTLL_powheg", "VV"]

for background in BACKGROUNDs:
    procs = []
    for signal in MASSPOINTs[:8]:
        command = f"python selectModels.py --signal {signal} --background {background}"
        proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        procs.append(proc)

    for proc in procs:
        proc.communicate()
        assert proc.returncode == 0

    for signal in MASSPOINTs[8:]:
        command = f"python selectModels.py --signal {signal} --background {background}"
        proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        procs.append(proc)

    for proc in procs:
        proc.communicate()
        assert proc.returncode == 0
