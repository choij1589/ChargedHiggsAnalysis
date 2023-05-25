import argparse
import ROOT as R
from math import sqrt, log
from array import array
from itertools import product
R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--era", required=True, type=str, help="era")
args = parser.parse_args()

SIGNAL = args.signal
ERA = args.era
CHANNEL = "Skim3Mu"
NETWORK = "GraphNet"

# List of backgrounds
nonprompt = ["nonprompt"]
conversion = ["DYJets", "DYJets10to50_MG", "ZGToLLG"]
diboson = ["WZTo3LNu_amcatnlo", "ZZTo4L_powheg"]
ttX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"]
others = ["GluGluHToZZTo4L", "VBF_HToZZTo4L",
          "WWW", "WWZ", "WZZ", "ZZZ", "WWG",
          "tZq", "tHq", "TTG", "TTTT"]
backgrounds = nonprompt + conversion + diboson + ttX + others

# fit results
sigma_dict = {65: 0.76,
              85: 1.03,
              90: 1.08,
              95: 1.19,
              120: 1.58}

def getScoreDistribution(sampleName):
    mA = int(SIGNAL.split("_")[1].split("-")[1])
    sigma = sigma_dict[mA]

    filepath = ""
    if sampleName == SIGNAL:
        filepath = f"/home/choij/workspace/ChargedHiggsAnalysis/data/PromptUnbinned/{ERA}/{CHANNEL}__{NETWORK}__/PromptUnbinned_TTToHcToWAToMuMu_{SIGNAL}.root"
    elif sampleName == "nonprompt":
        filepath = f"/home/choij/workspace/ChargedHiggsAnalysis/data/MatrixUnbinned/{ERA}/{CHANNEL}__{NETWORK}__/DATA/MatrixUnbinned_SkimTree_SS2lOR3l_DoubleMuon.root"
    else:
        filepath = f"/home/choij/workspace/ChargedHiggsAnalysis/data/PromptUnbinned/{ERA}/{CHANNEL}__{NETWORK}__/PromptUnbinned_SkimTree_SS2lOR3l_{sampleName}.root"
    f = R.TFile(filepath)
    tree = f.Get("Events_Central")

    mass1 = array("d", [0.]);       tree.SetBranchAddress("mass1", mass1)
    mass2 = array("d", [0.]);       tree.SetBranchAddress("mass2", mass2)
    scoreX = array("d", [0.]);      tree.SetBranchAddress(f"score_{SIGNAL}_vs_nonprompt", scoreX)
    scoreY = array("d", [0.]);      tree.SetBranchAddress(f"score_{SIGNAL}_vs_diboson", scoreY)
    scoreZ = array("d", [0.]);      tree.SetBranchAddress(f"score_{SIGNAL}_vs_ttZ", scoreZ)
    weight = array("d", [0.]);      tree.SetBranchAddress("weight", weight)

    h = R.TH3D(f"score_{sampleName}", "", 100, 0., 1., 100, 0., 1., 100, 0., 1.)
    for evt in range(tree.GetEntries()):
        tree.GetEntry(evt)
        condition = (mA - 5*sigma < mass1[0] < mA + 5*sigma) or (mA - 5*sigma < mass2[0] < mA + 5*sigma)
        if not condition: continue

        h.Fill(scoreX[0], scoreY[0], scoreZ[0], weight[0])
    h.SetDirectory(0)
    f.Close()
    return h

h_sig = getScoreDistribution(SIGNAL)

h_bkg = None
for bkg in backgrounds:
    h = getScoreDistribution(bkg)
    if h_bkg is None: h_bkg = h.Clone("score_bkg")
    else:             h_bkg.Add(h)

nbinsX = h_sig.GetNbinsX()
nbinsY = h_sig.GetNbinsY()
nbinsZ = h_sig.GetNbinsZ()

nSig = h_sig.Integral(0, nbinsX+1, 0, nbinsY+1, 0, nbinsZ+1) / 3
nBkg = h_bkg.Integral(0, nbinsX+1, 0, nbinsY+1, 0, nbinsZ+1)
initMetric = sqrt(2*((nSig+nBkg)*log(1+nSig/nBkg)-nSig))
print(initMetric)

bestBinX = 0
bestBinY = 0
bestBinZ = 0
bestMetric = initMetric
for binX, binY, binZ in product(range(nbinsX+1), range(nbinsY+1), range(nbinsZ+1)):
    nSig = h_sig.Integral(binX, nbinsX, binY, nbinsY, binZ, nbinsZ) / 3
    nBkg = h_bkg.Integral(binX, nbinsX, binY, nbinsY, binZ, nbinsZ)
    try:
        metric = sqrt(2*((nSig+nBkg)*log(1+nSig/nBkg)-nSig))
    except Exception as e:
        print(f"nSig = {nSig}, nBkg = {nBkg}")
        print(e)
        continue
    
    if metric > bestMetric:
        bestBinX = binX
        bestBinY = binY
        bestBinZ = binZ
        bestMetric = metric
print(bestBinX, bestBinY, bestBinZ, bestMetric)
print((bestMetric-initMetric) / initMetric)
