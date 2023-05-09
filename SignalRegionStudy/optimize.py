import os, shutil
import argparse
import ROOT
import pandas as pd
WORKDIR = os.getenv("WORKDIR")
ROOT.gSystem.Load(f"{WORKDIR}/libCpp/prepareDataFrame_cc.so")
ROOT.gSystem.Load(f"{WORKDIR}/libCpp/optimize_cc.so")
ROOT.EnableImplicitMT(8)

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--network", required=True, type=str, help="network")
parser.add_argument("--xsec", default=15., type=float, help="signal xsec")
args = parser.parse_args()

# constants
ERA = args.era
CHANNEL = args.channel
NETWORK = args.network
MASSPOINT = args.signal

# perpare output directories
print(f"@@@@ Optimizing {MASSPOINT}...")
outDir = f"{WORKDIR}/SignalRegionStudy/{ERA}/{CHANNEL}__{NETWORK}__/{MASSPOINT}"
if not os.path.exists(outDir):
    os.makedirs(outDir)

# preprocess samples with central weights to optimize score cuts
# conversion = ["DYJets", "DYJets10to50_MG", "ZGToLLG"]
# diboson = ["WZTo3LNu_amcatnlo","ZZTo4L_powheg"]
# ttX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"]
# others = ["WWW", "WWZ", "WZZ", "ZZZ", "TTG", "tZq", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]
# nonskim = ["TTTT", "WWG", "tHq"]
# MCSamples = conversion + diboson + ttX + others

# make RDataFrame for each sample
# ROOT.prepareOptimization(ERA, CHANNEL, NETWORK, MASSPOINT, MASSPOINT, True, False, False)
# ROOT.prepareOptimization(ERA, CHANNEL, NETWORK, MASSPOINT, "Nonprompt", False, True, True)
# for sample in MCSamples:
#     ROOT.prepareOptimization(ERA, CHANNEL, NETWORK, MASSPOINT, sample, False, False, True)
# for sample in nonskim:
#     ROOT.prepareOptimization(ERA, CHANNEL, NETWORK, MASSPOINT, sample, False, False, False)

# read fit information
csv = pd.read_csv(f"{args.era}/{args.channel}__/fitResults.csv", index_col=["masspoint"])

mA = float(csv.loc[args.signal, 'mA'])
sigma = float(csv.loc[args.signal, 'sigma'])
width = float(csv.loc[args.signal, 'width'])

# check whether file exists
if not os.path.exists(f"{outDir}/results.csv"):
    with open(f"{outDir}/results.csv", "w") as f:
        f.write("# xsec, metric, bestMetric, xcut, ycut\n")

out = ROOT.optimize(args.era, args.channel, args.network, args.signal, args.xsec, mA, sigma, width)
metric = out.at(0)
bestMetric = out.at(1)
xcut = out.at(2)
ycut = out.at(3)
with open(f"{outDir}/results.csv", "a") as f:
    f.write(f"{args.xsec}, {metric}, {bestMetric}, {xcut}, {ycut}\n")
