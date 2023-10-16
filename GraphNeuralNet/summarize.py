import os, shutil
import pandas as pd
from itertools import product

WORKDIR = os.environ["WORKDIR"]
CHANNEL = "Skim3Mu"

EPOCHs = {"MHc-100_MA-95_vs_nonprompt": 50,
          "MHc-130_MA-90_vs_nonprompt": 120,
          "MHc-160_MA-85_vs_nonprompt": 80,
          "MHc-100_MA-95_vs_diboson": 120,
          "MHc-130_MA-90_vs_diboson": 120,
          "MHc-160_MA-85_vs_diboson": 120,
          "MHc-100_MA-95_vs_ttZ": 120,
          "MHc-130_MA-90_vs_ttZ": 120,
          "MHc-160_MA-85_vs_ttZ": 120}

os.makedirs(f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/summary/models", exist_ok=True)
os.makedirs(f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/summary/info", exist_ok=True)

for modelkey, epoch in EPOCHs.items():
    csv = pd.Series(pd.read_csv(f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/epoch{epoch}/{modelkey}/results/summary.txt", header=None, sep=",\s", engine="python").transpose()[0])
    modelIdx, nNodes, optimizer, initLR, scheduler = csv[2:7]
    print(modelIdx, nNodes, optimizer, initLR, scheduler)
    
    # copy summary
    init_path = f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/epoch{epoch}/{modelkey}/results/summary.txt"
    copy_path = f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/summary/info/{modelkey}.txt"
    shutil.copy2(init_path, copy_path)
    
    # copy ROC plots
    init_path = f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/epoch{epoch}/{modelkey}/results/ROC-model{modelIdx}.png"
    copy_path = f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/summary/info/ROC-{modelkey}.png"
    shutil.copy2(init_path, copy_path)
    
    # copy training procedure
    init_path = f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/epoch{epoch}/{modelkey}/results/training-model{modelIdx}.png"
    copy_path = f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/summary/info/training-{modelkey}.png"
    shutil.copy2(init_path, copy_path)

    # copy models
    init_path = f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/epoch{epoch}/{modelkey}/models/ParticleNet-nNodes{nNodes}_{optimizer}_initLR-{str(initLR).replace('.', 'p')}_{scheduler}.pt"
    copy_path = f"{WORKDIR}/GraphNeuralNet/{CHANNEL}/summary/models/{modelkey}.pt"
    shutil.copy2(init_path, copy_path)