import os, shutil
import argparse
from ROOT import TFile

parser = argparse.ArgumentParser()
parser.add_argument("--era", "-e", type=str, required=True, help="Era")
parser.add_argument("--flag", "-f", type=str, required=True, help="SKFlatAnalyzer flag")
args = parser.parse_args()

prefix = f"{args.era}/{args.flag}"

# read sample list
sampleList = []
with open(f"sampleList.txt", "r") as f:
    for line in f.readlines():
        if line[0] == "#" in line:
            continue
        sampleList.append(line[:-1])

# make split directory
if not os.path.exists(f"{prefix}/Split"):
    os.makedirs(f"{prefix}/Split")

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
