import os, shutil
import argparse
import ROOT
WORKDIR = os.getenv("WORKDIR")
ROOT.gSystem.Load(f"{WORKDIR}/libCpp/fitAmass_cc.so")
ROOT.gSystem.Load(f"{WORKDIR}/libCpp/prepareDataFrame_cc.so")
ROOT.EnableImplicitMT(4)

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--network", required=True, type=str, help="network")
args = parser.parse_args()

# constants
ERA = args.era
CHANNEL = args.channel
NETWORK = args.network
MASSPOINT = args.signal

# fit a mass
#fitResult = ROOT.fitAmass("2017", "MHc-70_MA-15", 15, 14, 16)
#mA = fitResult.at(0).getValV()
#sigma = fitResult.at(1).getValV()
#width = fitResult.at(2).getValV()

# prepare output directories
print(f"@@@@ Preprocessing {MASSPOINT}...")
outDir = f"{ERA}/{CHANNEL}__{NETWORK}__/{MASSPOINT}"
if not os.path.exists(outDir):
    os.makedirs(outDir)

# preprocess samples with central weights to optimize score cuts
conversion = ["DYJets", "DYJets10to50_MG", "ZGToLLG"]
diboson = ["WZTo3LNu_amcatnlo","ZZTo4L_powheg"]
ttX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"]
others = ["WWW", "WWZ", "WZZ", "ZZZ", "TTG", "tZq", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]
nonskim = ["TTTT", "WWG", "tHq"]
MCSamples = conversion + diboson + ttX + others

# make RDataFrame for each sample
ROOT.prepareOptimization(ERA, CHANNEL, NETWORK, MASSPOINT, MASSPOINT, True, False, False)
ROOT.prepareOptimization(ERA, CHANNEL, NETWORK, MASSPOINT, "Nonprompt", False, True, True)
for sample in MCSamples:
    ROOT.prepareOptimization(ERA, CHANNEL, NETWORK, MASSPOINT, sample, False, False, True)
for sample in nonskim:
    ROOT.prepareOptimization(ERA, CHANNEL, NETWORK, MASSPOINT, sample, False, False, False)
