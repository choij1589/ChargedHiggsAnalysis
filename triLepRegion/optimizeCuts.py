import argparse
import numpy as np
from math import sqrt, log
from itertools import product
from ROOT import TFile

parser = argparse.ArgumentParser()
parser.add_argument("--channel", required=True)
parser.add_argument("--masspoint", required=True)
args = parser.parse_args()

mA = int(args.masspoint.split("_")[1].split("-")[1])
HOME = "/home/choij/workspace/ChargedHiggsAnalysis"
NONPROMPTs = ["DYJets", "DYJets10to50_MG", "TTLL_powheg"]
VVs = ["WZTo3LNu_amcatnlo", "ZZTo4L_powheg"]
TTXs = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"]
CONVs = ["ZGToLLG", "TTG"]
RAREs = ["WWW", "WWZ", "WZZ", "ZZZ", "GluGluHToZZTo4L", "VBF_HToZZTo4L"]
BACKGROUNDs = NONPROMPTs+VVs+TTXs+CONVs+RAREs

# get histograms
histkey = f"{args.channel}/{args.masspoint}/3D"
f = TFile.Open(f"{HOME}/ValidParticleNet/Signals/TTToHcToWAToMuMu_{args.masspoint}.root")
h_sig = f.Get(histkey); h_sig.SetDirectory(0)
f.Close()

hists = {}
for bkg in BACKGROUNDs:
    f = TFile.Open(f"{HOME}/ValidParticleNet/Backgrounds/{bkg}.root")
    h_bkg = f.Get(histkey); h_bkg.SetDirectory(0)
    f.Close()
    hists[bkg] = h_bkg

def getNumberOfEvts(mA, cuts):
    mAcut, fcut, xcut = cuts
    xL, xR = h_sig.GetXaxis().FindBin(mA-mAcut), h_sig.GetXaxis().FindBin(mA+mAcut)
    yL, yR = h_sig.GetYaxis().FindBin(fcut), h_sig.GetYaxis().FindBin(1.)
    zL, zR = h_sig.GetZaxis().FindBin(xcut), h_sig.GetZaxis().FindBin(1.)
    
    # signal
    nSig = h_sig.Integral(xL, xR, yL, yR, zL, zR)
    
    # background
    nBkg = 0.
    for bkg in BACKGROUNDs:
        thisBkg = hists[bkg].Integral(xL, xR, yL, yR, zL, zR)
        if thisBkg < 0.:
            #print(f"negative bkgs for {bkg}")
            continue
        else:
            nBkg += thisBkg
    return (nSig, nBkg)

def getMetric(nSig, nBkg):
    return sqrt(2*((nSig+nBkg)*log(1+nSig/nBkg) - nSig))

mAcuts = np.linspace(0, 5, 51)
fcuts = np.linspace(0, 1, 21)
xcuts = np.linspace(0, 1, 21)

# 1D
metric = -1.
bestMAcut = 0.
for mAcut in mAcuts:
    nSig, nBkg = getNumberOfEvts(mA=mA, cuts=[mAcut, 0., 0.])
    try:
        thisMetric = getMetric(nSig, nBkg)
        if thisMetric > metric: 
            metric = thisMetric
            bestMAcut = mAcut
    except Exceptions as e:
        print(e)
print(f"1D Optimization: {metric} with best MA cut {bestMAcut}")

metric = -1.
bestMAcut = 0.
bestFcut = 0.
bestXcut = 0.
for mAcut, fcut, xcut in product(mAcuts, xcuts, fcuts):
    nSig, nBkg = getNumberOfEvts(mA=mA, cuts=[mAcut, fcut, xcut])
    try:
        thisMetric = getMetric(nSig, nBkg)
        if thisMetric > metric: 
            metric = thisMetric
            bestMAcut = mAcut
            bestFcut = fcut
            bestXcut = xcut
    except Exception as e:
        print(e)
