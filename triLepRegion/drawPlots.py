import os
import argparse

from math import pow, sqrt
from ROOT import kBlack, kYellow, kGray, kRed, kBlue, kGreen, kMagenta, kCyan, kAzure, kViolet
from ROOT import TFile
from Plotter import KinematicCanvas, ComparisonCanvas

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--obs", required=True, type=str, help="observable")
parser.add_argument("--region", required=True, type=str, help="SR / CR name")
parser.add_argument("--blind", action="store_true", help="blind mode")
args = parser.parse_args()

WORKDIR = os.environ['WORKDIR']

config = {"xTitle": "m(A)",
          "yTitle": "Events / 5 GeV",
          "xRange": [70., 120.],
          #"rebin": 5,
          "logy": False}
config["era"] = args.era

# Sample List
if "1E2Mu" in args.region: DataStream = "MuonEG"
elif "3Mu" in args.region: DataStream = "DoubleMuon"
else: print(f"wrong region {args.region}"); exit(1)
NonPrompt = ["DYJets", "DYJets10to50_MG", "TTLL_powheg"]
Conv = ["ZGToLLG", "TTG"]
VV = ["WZTo3LNu_amcatnlo", "ZZTo4L_powheg"]
ttX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb", "tZq", "tHq"]
Rare = ["WWW", "WWZ", "WZZ", "ZZZ", "WWG", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]
MCSamples = NonPrompt + Conv + VV + ttX + Rare

MASSPOINTs = ["MHc-70_MA-15", "MHc-100_MA-60", "MHc-130_MA-90", "MHc-160_MA-155"]
SYSTEMATICs = ["Central"]

# get histograms
SIGs = {}
BKGs = {}
colors = {}

# data
f = TFile.Open(f"{WORKDIR}/ValidParticleNet/{args.era}/ValidParticleNet_{DataStream}.root")
data = f.Get(f"{args.region}/{args.obs}"); data.SetDirectory(0)
f.Close()

# signals
for masspoint in MASSPOINTs:
    fstring =f"{WORKDIR}/ValidParticleNet/{args.era}/ValidParticleNet_TTToHcToWAToMuMu_{masspoint}.root" 
    assert os.path.exists(fstring)
    f = TFile.Open(fstring)
    try:
        h = f.Get(f"{args.region}/{args.obs}"); h.SetDirectory(0)
        f.Close()
        SIGs[masspoint] = h.Clone(masspoint); del h
    except Exception as e:
        print(masspoint, e)

# backgrounds
histograms = {}
for sample in MCSamples:
    fstring = f"{WORKDIR}/ValidParticleNet/{args.era}/ValidParticleNet_{sample}.root"
    if not os.path.exists(fstring):
        fstring = f"{WORKDIR}/ValidParticleNet/{args.era}/ValidParticleNet_SkimTree_SS2lOR3l_{sample}.root" 
    assert os.path.exists(fstring)
    f = TFile.Open(fstring)
    try:
        h = f.Get(f"{args.region}/{args.obs}"); h.SetDirectory(0)
        f.Close()
        histograms[sample] = h.Clone(sample); del h
    except Exception as e:
        print(sample, e)

# merge backgrounds
def addHist(name, hist, histDict):
    if histDict[name] is None:
        histDict[name] = hist.Clone(name)
    else:
        histDict[name].Add(hist)

BKGs['rare'] = None
BKGs['conv'] = None
BKGs['VV'] = None
BKGs['ttX'] = None
BKGs['fake'] = None

for sample in NonPrompt:
    if not sample in histograms.keys(): continue
    addHist("fake", histograms[sample], BKGs)
for sample in Conv: 
    if not sample in histograms.keys(): continue
    addHist("conv", histograms[sample], BKGs)
for sample in VV:
    if not sample in histograms.keys(): continue
    addHist("VV", histograms[sample], BKGs)
for sample in ttX:
    if not sample in histograms.keys(): continue
    addHist("ttX", histograms[sample], BKGs)
for sample in Rare:
    if not sample in histograms.keys(): continue
    addHist("rare", histograms[sample], BKGs)
    
# colors
colors['data'] = kBlack
colors['rare'] = kMagenta
colors['conv'] = kGreen
colors['VV'] = kAzure
colors['ttX'] = kViolet
colors['fake'] = kGray+100

colorList = [kGray, kBlue, kBlack, kRed]
for i, masspoint in enumerate(MASSPOINTs):
    colors[masspoint] = colorList[i]
    
# draw plots
if args.blind:
    c = KinematicCanvas(config=config)
    c.drawSignals(SIGs, colors)
    c.drawBackgrounds(BKGs, colors)
    c.drawLegend()
    c.finalize()
    c.savefig(f"{WORKDIR}/triLepRegion/test.png")
else:
    c = ComparisonCanvas(config=config)
    c.drawSignals(SIGs, colors)
    c.drawBackgrounds(BKGs, colors)
    c.drawData(data)
    c.drawRatio()
    c.drawLegend()
    c.finalize()
    c.savefig(f"{WORKDIR}/triLepRegion/test.png")
