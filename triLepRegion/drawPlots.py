import os
import argparse

from math import pow, sqrt
from ROOT import kBlack, kYellow, kGray, kRed, kBlue, kGreen, kMagenta, kCyan, kAzure, kViolet
from ROOT import TFile

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--obs", required=True, type=str, help="observable")
parser.add_argument("--region", required=True, type=str, help="SR / CR name")
args = parser.parse_args()

WORKDIR = os.environ['WORKDIR']

config = {"xTitle": "m(A)",
          "yTitle": "Events / 5 GeV",
          "xRange": [0., 200.],
          "rebin": 2,
          "logY": True}
config["era"] = args.era

# Sample list
DataStream = "DoubleMoun"
NonPrompt = ["DYJets", "DYJets10to50_MG", "TTLL_powheg"]
Conv = ["ZGToLLG", "TTG"]
VV = ["WZTo3LNu_amcatnlo", "ZZTo4L_powheg"]
ttX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb", "tZq", "tHq"]
Rare = ["WWW", "WWZ", "WZZ", "ZZZ", "WWG", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]
MCSamples = NonPrompt + Conv + VV + ttX + Rare

MASSPOINTs = ["MHc-70_MA-15", "MHc-100_MA-60", "MHc-130_MA-90", "MHc-160_MA-155"]
SYSTEMATICs = ["Central"]

# get histograms
# signals
SIGs = {}
for masspoint in MASSPOINTs:
    fstring =f"{WORKDIR}/ValidParticleNet/{args.era}/ValidParticleNet_TTToHcToWAToMuMu_{masspoint}.root" 
    assert os.path.exists(fstring)
    f = TFile.Open(fstring)
    h = f.Get(f"{args.region}/{args.obs}"); h.SetDirectory(0)
    f.Close()
    SIGs[masspoint] = h.Clone(masspoint); del h

# backgrounds
BKGs = {}
for sample in MCSamples:
    fstring = f"{WORKDIR}/ValidParticleNet/{args.era}/ValidParticleNet_{sample}.root"
    if not os.path.exists(fstring):
        fstring = f"{WORKDIR}/ValidParticleNet/{args.era}/ValidParticleNet_SkimTree_SS2lOR3l_{sample}.root" 
    assert os.path.exists(fstring)
    f = TFile.Open(fstring)
    h = f.Get(f"{args.region}/{args.obs}"); h.SetDirectory(0)
    f.Close()
    BKGs[sample] = h.Clone(sample); del h

# merge backgrounds
def addHist(name, hist, histDict):
    if histDict[name] is None:
        histDict[name] = hist.Clone(name)
    else:
        histDict[name].Add(hist)

colors = {}
colorList = [kRed, kGreen, kGray, kCyan]
for i, masspoint in enumerate(MASSPOINTs):
    colors[masspoint] = colorList[i]

histograms = {}
histograms['rare'] = None
histograms['conv'] = None
histograms['ttX'] = None
histograms['VV'] = None
histograms['fake'] = None

for sample in NonPrompt:
    if not sample in BKGs.keys(): continue
    addHist("fake", BKGs[sample], histograms)
for sample in Conv: 
    if not sample in BKGs.keys(): continue
    addHist("conv", BKGs[sample], histograms)
for sample in VV:
    if not sample in BKGs.keys(): continue
    addHist("VV", BKGs[sample], histograms)
for sample in ttX:
    if not sample in BKGs.keys(): continue
    addHist("ttX", BKGs[sample], histograms)
for sample in Rare:
    if not sample in BKGs.keys(): continue
    addHist("rare", BKGs[sample], histograms)
    
# colors
colors['fake'] = kGray
colors['conv'] = kCyan
colors['VV'] = kGreen
colors['ttX'] = kBlue
colors['rare'] = kRed

for name, color in colors.items():
    print(name, color)

# draw plots
from Plotter import KinematicCanvas
c = KinematicCanvas(config=config)
c.drawSignals(SIGs, colors)
c.drawBackgrounds(histograms, colors)
c.drawLegend()
c.finalize()
c.savefig(f"{WORKDIR}/triLepRegion/test.png")
