import os, sys; sys.path.insert(0, os.environ['WORKDIR'])
import shutil
import argparse
from ROOT import TFile
from ROOT import TTree

parser = argparse.ArgumentParser()
parser.add_argument("--flag", "-f", required=True, type=str, help="SKFlatAnalyzer flag")
parser.add_argument("--force", action="store_true", default=False, help="remove Training directory?")
args = parser.parse_args()

if args.flag == "Skim1E2Mu":
    SampleInfo = {
        "TTToHcToWA":  [25000, 25000, 50000, 50000],
        "TTLL_powheg": [25000, 25000, 50000, 50000],
        "ttWToLNu":    [6000, 6000, 12000, 12000],
        "ttZToLLNuNu": [18000, 18000, 36000, 36000],
        "ttHToNonbb":  [6000, 6000, 12000, 12000]
        }
elif args.flag == "Skim3Mu":
    SampleInfo = {
        "TTToHcToWA":  [25000, 25000, 50000, 50000],
        "TTLL_powheg": [25000, 25000, 50000, 50000],
        "ttWToLNu":    [4500, 4500, 9000, 9000],
        "ttZToLLNuNu": [21000, 21000, 42000, 42000],
        "ttHToNonbb":  [4500, 4500, 9000, 9000]
        }
else:
    print(f"@@@@ Wrong flag {args.flag}")
    raise(KeyError)

MASSPOINTs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
              "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
              "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
              "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
BACKGROUNDs = ["TTLL_powheg", "ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"]
ERAs = ["2016preVFP", "2016postVFP", "2017", "2018"]

#### helper functions
def checkEvtEntries(sampleName, era):
    idx = ERAs.index(era)
    key = sampleName
    if "TTToHcToWA" in sampleName:
        key = "TTToHcToWA"
    entriesToVerify = SampleInfo[key][idx]
    
    f = TFile.Open(f"{era}/{args.flag}__/Selector_{sampleName}.root")
    tree = f.Get("Events")
    entries = tree.GetEntries()
    f.Close()
    if entries > entriesToVerify:
        return True
    else:
        return False

def haddSamples(sampleName):
    key = sampleName
    if "TTToHcToWA" in sampleName:
        key = "TTToHcToWA"
    EntriesToCopy = SampleInfo[key]

    for idx, era in enumerate(ERAs):
        entry = EntriesToCopy[idx]
        copyFile = f"{os.environ['WORKDIR']}/libCpp/copyFile"
        command = f"{copyFile} {era}/{args.flag}__/Selector_{sampleName}.root {entry}"
        os.system(command)
        start = f"{era}/{args.flag}__/Selector_{sampleName}_copy.root"
        end = f"Training/Selector_{sampleName}_{era}.root"
        shutil.move(start, end)
    command = f"hadd Training/{args.flag}__/Selector_{sampleName}.root Training/Selector_{sampleName}_*.root"
    os.system(command)
    for era in ERAs:
        os.remove(f"Training/Selector_{sampleName}_{era}.root")


#### check all files
for mp in MASSPOINTs:
    sampleName = f"TTToHcToWAToMuMu_{mp}"
    for era in ERAs:
        assert checkEvtEntries(sampleName, era)
for bkg in BACKGROUNDs:
    for era in ERAs:
        assert checkEvtEntries(bkg, era)
print("@@@@ number of events for all files are passed")

#### now hadd files
if args.force and os.path.exists(f"Training/{args.flag}__"):
    shutil.rmtree(f"Training/{args.flag}__")
os.makedirs(f"Training/{args.flag}__")
for mp in MASSPOINTs:
    sampleName = f"TTToHcToWAToMuMu_{mp}"
    haddSamples(sampleName)
for bkg in BACKGROUNDs:
    haddSamples(bkg)

