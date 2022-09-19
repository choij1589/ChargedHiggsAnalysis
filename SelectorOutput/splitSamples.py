import os, shutil
from ROOT import TFile

prefix = "Skim3Mu__"

# read sample list
sampleList = []
with open("SampleList.txt", "r") as f:
    for line in f.readlines():
        if line[0] == "#" or "DoubleMuon" in line:
            continue
        sampleList.append(line[:-1])

# make split directory
if not os.path.exists(f"{prefix}/Split"):
    os.makedirs("{prefix}/Split")

def splitSample(samplename):
    # open file
    f = TFile.Open(f"{prefix}/Selector_{samplename}.root")
    entries = f.Events.GetEntries()
    f.Close()
    
    # decide the number of splitted files
    if entries < 10000:
        shutil.copy(f"{prefix}/Selector_{samplename}.root", f"{prefix}/Split/Selector_{samplename}_0.root")
    else:
        nfiles = int(entries/10000)
        command = f"{os.environ['WORKDIR']}/libCpp/splitFile {prefix}/Selector_{samplename}.root {nfiles}"
        print(command)
        os.system(command)
        for idx in range(nfiles):
            shutil.move(f"{prefix}/Selector_{samplename}_{idx}.root", f"{prefix}/Split/Selector_{samplename}_{idx}.root")

for sample in sampleList:
    splitSample(sample)

