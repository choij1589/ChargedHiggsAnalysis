import os
import argparse
import numpy as np
import ROOT
import uuid
from itertools import product
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--masspoint", required=True, type=str, help="signal masspoint")
parser.add_argument("--network", required=True, type=str, help="network type")
args = parser.parse_args()

ERA = args.era
MASSPOINT = args.masspoint
CHANNEL = args.channel
NETWORK = args.network
WORKDIR = os.environ['WORKDIR']

if CHANNEL == "Skim1E2Mu":
    DataStream = "MuonEG"
elif CHANNEL == "Skim3Mu":
    DataStream = "DoubleMuon"
else:
    print(f"Wrong argument {args.channel}")
    exit(1)

SYSTEMATICs = ["Nonprompt",
               "Conversion",
               "L1Prefire", 
               "PileupReweight", 
               "MuonIDSF", 
               "DblMuTrigSF"]

conv        = ["DYJets", "ZGToLLG"]
VV          = ["WZTo3LNu_amcatnlo","ZZTo4L_powheg"]
ttX         = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"]
rare        = ["WWW", "WWZ", "WZZ", "ZZZ","WWG", "TTG", "TTTT", "tZq", "tHq", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]

SIGMAs = {"MHc-70_MA-15": 0.106033,
          "MHc-70_MA-40": 0.298239,
          "MHc-70_MA_65": 0.531261,
          "MHc-100_MA-15": 0.105649,
          "MHc-100_MA-60": 0.459994,
          "MHc-100_MA-95": 0.822346,
          "MHc-130_MA-15": 0.107722,
          "MHc-130_MA-55": 0.397281,
          "MHc-130_MA-90": 0.743059,
          "MHc-130_MA-125": 1.173,
          "MHc-160_MA-15": 0.111555,
          "MHc-160_MA-85": 0.675834,
          "MHc-160_MA-120": 1.10671,
          "MHc-160_MA-155": 1.54566
          }
WIDTHs = {"MHc-70_MA-15": 0.138704,
          "MHc-70_MA-40": 0.426343,
          "MHc-70_MA_65": 0.790565,
          "MHc-100_MA-15": 0.134165,
          "MHc-100_MA-60": 0.698251,
          "MHc-100_MA-95": 1.27854,
          "MHc-130_MA-15": 0.134053,
          "MHc-130_MA-55": 0.652921,
          "MHc-130_MA-90": 1.15738,
          "MHc-130_MA-125": 1.76685,
          "MHc-160_MA-15": 0.138476,
          "MHc-160_MA-85": 1.11303,
          "MHc-160_MA-120": 1.64523,
          "MHc-160_MA-155": 2.45647
          }


MA = float(MASSPOINT.split("_")[1].split("-")[1])
SIGMA = SIGMAs[MASSPOINT]
WIDTH = WIDTHs[MASSPOINT]
WINDOW = np.sqrt(np.power(SIGMA, 2)+np.power(WIDTH, 2))

if "2016" in args.era:
    ConvSF = {"LowPT3Mu": [0.906, 0.878],
              "HighPT3Mu": [2.003, 0.739]}
elif args.era == "2017":
    ConvSF = {"LowPT3Mu": [0.901, 1.303],
              "HighPT3Mu": [1.239, 0.464]}
elif args.era == "2018":
    ConvSF = {"LowPT3Mu": [0.628, 0.522],
              "HighPT3Mu": [0.981, 0.412]}

#### helper functions
def getEventRates(fstring: str, histkey: str, xcut=0.73, ycut=0.87) -> float:
    f = ROOT.TFile.Open(fstring)
    # Get event rates
    h = f.Get(histkey); h.SetDirectory(0)
    f.Close()

    xL = h.GetXaxis().FindBin(MA-WINDOW)
    xR = h.GetXaxis().FindBin(MA+WINDOW)
    h.GetXaxis().SetRange(xL, xR)

    hProj = h.Project3D(f"{uuid.uuid4().hex.upper()[:6]}_yz")
    rates = 0.
    for xbin, ybin in product(range(hProj.GetNbinsX()+1), range(hProj.GetNbinsY()+1)):
        scoreX = hProj.GetXaxis().GetBinCenter(xbin)
        scoreY = hProj.GetYaxis().GetBinCenter(ybin)
        if scoreX < xcut: continue
        if scoreY < ycut: continue
        thisBin = hProj.FindBin(scoreX, scoreY)
        rates += hProj.GetBinContent(thisBin)

    return rates

#### get event rates
RATEs = {}
# observation
fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__/DATA/PromptEstimator_SkimTree_SS2lOR3l_{DataStream}.root"
histkey = f"SR3Mu/Central/{MASSPOINT}/3D"
assert os.path.exists(fstring)
RATEs["observation"] = getEventRates(fstring, histkey)

# signal
fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_TTToHcToWAToMuMu_{MASSPOINT}.root"
assert os.path.exists(fstring)
histkey = f"SR3Mu/Central/{MASSPOINT}/3D"
RATEs["signal"] = {}
rate = getEventRates(fstring, histkey)
RATEs["signal"]["Central"] = rate
for syst in SYSTEMATICs:
    if syst in ["Nonprompt", "Conversion"]:
        RATEs["signal"][syst] = "-"
    else:
        rateUp = getEventRates(fstring, histkey.replace("Central", f"{syst}Up"))
        rateDown = getEventRates(fstring, histkey.replace("Central", f"{syst}Down"))
        RATEs["signal"][syst] = max( abs(rateUp - rate), abs(rateDown - rate) ) / rate + 1. 

# nonprompt
fstring = f"{WORKDIR}/data/NonpromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__/DATA/NonpromptEstimator_SkimTree_SS2lOR3l_DoubleMuon.root"
assert os.path.exists(fstring)
RATEs["nonprompt"] = {}
histkey = f"SR3Mu/Central/{MASSPOINT}/3D"
rate = getEventRates(fstring, histkey)
rateUp = getEventRates(fstring, histkey.replace("Central", "NonpromptUp"))
rateDown = getEventRates(fstring, histkey.replace("Central", "NonpromptDown"))
RATEs["nonprompt"]["Central"] = rate
for syst in SYSTEMATICs:
    if syst == "Nonprompt":
        RATEs["nonprompt"][syst] = max( abs(rateUp - rate), abs(rateDown - rate) ) / rate + 1.
    else:
        RATEs["nonprompt"][syst] = "-"

# diboson
rate = 0.
for sample in VV:
    fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_{sample}.root"
    assert os.path.exists(fstring)
    histkey = f"SR3Mu/Central/{MASSPOINT}/3D"
    rate += max(0., getEventRates(fstring, histkey))
RATEs["diboson"] = {}
RATEs["diboson"]["Central"] = rate

for syst in SYSTEMATICs:
    if syst in ["Nonprompt", "Conversion"]:
        RATEs["diboson"][syst] = "-"
        continue
    rate = RATEs["diboson"]["Central"]
    rateUp = 0.
    rateDown = 0.
    for sample in VV:
        fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_{sample}.root"
        assert os.path.exists(fstring)
        rateUp += max(0., getEventRates(fstring, f"SR3Mu/{syst}Up/{MASSPOINT}/3D"))
        rateDown += max(0., getEventRates(fstring, f"SR3Mu/{syst}Down/{MASSPOINT}/3D"))
    RATEs["diboson"][syst] = max( abs(rateUp - rate), abs(rateDown - rate) ) / rate + 1.

#### conversion
rate = 0.
rateUp = 0.
rateDown = 0.
# DYJets
fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_DYJets.root"
assert os.path.exists(fstring)
histkey = f"SR3Mu/Central/{MASSPOINT}/3D"
rate += max(0., getEventRates(fstring, histkey))
rateUp += max(0., rate * (ConvSF["LowPT3Mu"][0]+ConvSF["LowPT3Mu"][1]))
rateDown += max(0., rate * (ConvSF["LowPT3Mu"][0]-ConvSF["LowPT3Mu"][1]))
# ZGToLLG
fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_ZGToLLG.root"
assert os.path.exists(fstring)
histkey = f"SR3Mu/Central/{MASSPOINT}/3D"
rate += max(0., getEventRates(fstring, histkey))
rateUp += max(0., rate * (ConvSF["HighPT3Mu"][0]+ConvSF["HighPT3Mu"][1]))
rateDown += max(0., rate * (ConvSF["HighPT3Mu"][0]-ConvSF["HighPT3Mu"][1]))

RATEs["conversion"] = {}
RATEs["conversion"]["Central"] = rate
try:
    RATEs["conversion"]["Conversion"] = max( abs(rateUp - rate), abs(rateDown - rate) ) / rate+ 1.
except:
    RATEs["conversion"]["Conversion"] = 1.

for syst in SYSTEMATICs:
    if syst == "Conversion": continue
    RATEs["conversion"][syst] = "-"

# ttX
rate = 0.
for sample in ttX:
    fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_{sample}.root"
    assert os.path.exists(fstring)
    histkey = f"SR3Mu/Central/{MASSPOINT}/3D"
    rate += max(0., getEventRates(fstring, histkey))
RATEs["ttX"] = {}
RATEs["ttX"]["Central"] = rate

for syst in SYSTEMATICs:
    if syst in ["Nonprompt", "Conversion"]:
        RATEs["ttX"][syst] = "-"
        continue
    rate = RATEs["ttX"]["Central"]
    rateUp = 0.
    rateDown = 0.
    for sample in ttX:
        fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_{sample}.root"
        assert os.path.exists(fstring)
        rateUp += max(0., getEventRates(fstring, f"SR3Mu/{syst}Up/{MASSPOINT}/3D"))
        rateDown += max(0., getEventRates(fstring, f"SR3Mu/{syst}Down/{MASSPOINT}/3D"))
    RATEs["ttX"][syst] = max( abs(rateUp - rate), abs(rateDown - rate) ) / rate + 1.

# rare
rate = 0.
for sample in rare:
    fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_{sample}.root"
    if not os.path.exists(fstring):
         fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_{sample}.root"
    assert os.path.exists(fstring)
    histkey = f"SR3Mu/Central/{MASSPOINT}/3D"
    rate += max(0., getEventRates(fstring, histkey))
RATEs["rare"] = {}
RATEs["rare"]["Central"] = rate

for syst in SYSTEMATICs:
    if syst in ["Nonprompt", "Conversion"]:
        RATEs["rare"][syst] = "-"
        continue
    rate = RATEs["rare"]["Central"]
    rateUp = 0.
    rateDown = 0.
    for sample in rare:
        fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_{sample}.root"
        if not os.path.exists(fstring):
         fstring = f"{WORKDIR}/data/PromptEstimator/{ERA}/{CHANNEL}__{NETWORK}__WeightVar__/PromptEstimator_{sample}.root"
        assert os.path.exists(fstring)
        rateUp += max(0., getEventRates(fstring, f"SR3Mu/{syst}Up/{MASSPOINT}/3D"))
        rateDown += max(0., getEventRates(fstring, f"SR3Mu/{syst}Down/{MASSPOINT}/3D"))
    RATEs["rare"][syst] = max( abs(rateUp - rate), abs(rateDown - rate) ) / rate + 1.
 
pprint(RATEs)


#### print datacard
print("imax\t1 number of bins")
print("jmax\t5 number of processes minus 1")
print("kmax\t* number of nuisance parameters")
print("------------------------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------------------------")
print("bin\tsignal_region")
print(f"observation\t{RATEs['observation']}")
print("bin\tsignal_region\tsignal_region\tsignal_region\tsignal_region\tsignal_region\tsignal_region")
print("process\tnonprompt\tdiboson\tconversion\ttt+X\trare\tsignal")
print("process\t1\t2\t3\t4\t5\t0")
print(f"rate\t{RATEs['nonprompt']['Central']}\t{RATEs['diboson']['Central']}\t{RATEs['conversion']['Central']}\t{RATEs['ttX']['Central']}\t{RATEs['rare']['Central']}\t{RATEs['signal']['Central']}")
print("------------------------------------------------------------------------------------------------------")
for syst in SYSTEMATICs:
    print(f"{syst}\tlnN\t{RATEs['nonprompt'][syst]}\t{RATEs['diboson'][syst]}\t{RATEs['conversion'][syst]}\t{RATEs['ttX'][syst]}\t{RATEs['rare'][syst]}\t{RATEs['signal'][syst]}")





