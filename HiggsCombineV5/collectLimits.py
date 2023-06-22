import argparse
import json
import ROOT
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("--era", type=str, required=True, help="era")
parser.add_argument("--channel", type=str, required=True, help="channel")
parser.add_argument("--method", type=str, required=True, help="used method")
args = parser.parse_args()

MASSPOINTs = ["MHc-100_MA-15", "MHc-70_MA-40", "MHc-130_MA-55", "MHc-100_MA-60",
              "MHc-70_MA-65", "MHc-160_MA-85", "MHc-130_MA-90", "MHc-100_MA-95",
              "MHc-160_MA-120", "MHc-130_MA-125", "MHc-160_MA-155"]

MASSPOINTsGNN = ["MHc-70_MA-65", "MHc-160_MA-85", "MHc-130_MA-90", "MHc-100_MA-95", "MHc-160_MA-120"]

def parseAsymptoticLimit(masspoint):
    BASEDIR = f"results/{args.era}/{args.channel}__{args.method}__/{masspoint}"
    f = ROOT.TFile(f"{BASEDIR}/higgsCombineTest.AsymptoticLimits.mH120.root")
    limit = f.Get("limit")
    values = {}
    for idx, entry in enumerate(limit): values[idx] = entry.limit
    f.Close()
    
    out = {}
    out["exp-2"] = values[0] * 5
    out["exp-1"] = values[1] * 5
    out["exp0"] = values[2] * 5
    out["exp+1"] = values[3] * 5
    out["exp+2"] = values[4] * 5
    out["obs"] = values[5] * 5
    return out

def readHybridNewResult(path):
    print(path)
    f = ROOT.TFile(path)
    limit = f.Get("limit")
    try:
        for entry in limit:
            out = entry.limit
    except Exception as e:
        print(e)
    f.Close()
    return out * 5

def parseHybridNewLimit(masspoint):
    BASEDIR = f"results/{args.era}/{args.channel}__{args.method}__/{masspoint}"
    
    if args.method == "GNNOptim" and (masspoint not in MASSPOINTsGNN):
        BASEDIR = f"results/{args.era}/{args.channel}__Shape__/{masspoint}"
        
    out = {}
    out["exp-2"] = readHybridNewResult(f"{BASEDIR}/higgsCombineTest.HybridNew.mH120.quant0.025.root")
    out["exp-1"] = readHybridNewResult(f"{BASEDIR}/higgsCombineTest.HybridNew.mH120.quant0.160.root")
    out["exp0"] = readHybridNewResult(f"{BASEDIR}/higgsCombineTest.HybridNew.mH120.quant0.500.root")
    out["exp+1"] = readHybridNewResult(f"{BASEDIR}/higgsCombineTest.HybridNew.mH120.quant0.840.root")
    out["exp+2"] = readHybridNewResult(f"{BASEDIR}/higgsCombineTest.HybridNew.mH120.quant0.975.root")
    out["obs"] = readHybridNewResult(f"{BASEDIR}/higgsCombineTest.HybridNew.mH120.root")
    return out

limits = {}
for masspoint in MASSPOINTs:
    print(masspoint)
    mA = masspoint.split("_")[1].split("-")[1]
    out = parseHybridNewLimit(masspoint)
    print(out)
    limits[mA] = out

pprint(limits)
with open(f"limits/limits.{args.era}.{args.channel}.HybridNew.{args.method}.json", "w") as f:
    json.dump(limits, f, indent=2)
