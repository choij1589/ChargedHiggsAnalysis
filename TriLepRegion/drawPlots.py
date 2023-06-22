import os
import argparse
import ROOT
from math import pow, sqrt
from Plotter import ComparisonCanvas, KinematicCanvas
from TriLepRegion.histConfigs import histConfigs

# NO graphics
ROOT.gROOT.SetBatch(True)

#### Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--key", required=True, type=str, help="histkey")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--network", default="GraphNet", type=str, help="ML model architecture (DenseNet / GraphNet)")
parser.add_argument("--blind", action="store_true", help="blind mode")
args = parser.parse_args()

WORKDIR = os.environ['WORKDIR']
config = histConfigs[args.key]
config["era"] = args.era
config["yRange"] = [0., 2.]

#### Sample list
DataStream = ""
if "1E2Mu" in args.channel: DataStream = "MuonEG"
if "3Mu" in args.channel: DataStream = "DoubleMuon"

CONV = ["DYJets", "ZGToLLG"]
VV = ["WZTo3LNu_amcatnlo", "ZZTo4L_powheg"]
TTX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"]
RARE = ["WWW", "WWZ", "WZZ", "ZZZ","WWG", "TTG", "tZq", "tHq", "TTTT", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]
MCSamples = CONV + VV + TTX + RARE

#### Conversion scale factor
if "2016" in args.era:
    ConvSF = {"LowPT3Mu": [0.902, 0.890],
              "HighPT3Mu": [2.003, 0.738]}
elif args.era == "2017":
    ConvSF = {"LowPT3Mu": [0.901, 1.303],
              "HighPT3Mu": [1.239, 0.464]}
elif args.era == "2018":
    ConvSF = {"LowPT3Mu": [0.628, 0.522],
              "HighPT3Mu": [0.981, 0.412]}
    
if "3Mu" in args.channel: 
    convSFLowPT = ConvSF["LowPT3Mu"]
    convSFHighPT = ConvSF["HighPT3Mu"]

if "MHc" in args.key:
    MASSPOINTs = [args.key.split("/")[0]]
else:
    MASSPOINTs = ["MHc-70_MA-15", "MHc-100_MA-60", "MHc-130_MA-90", "MHc-160_MA-155"]
#### Systematics
SYSTEMATICs = [["L1PrefireUp", "L1PrefireDown"],
               ["PileupReweightUp", "PileupReweightDown"],
               ["MuonIDSFUp", "MuonIDSFDown"],
               ["DblMuTrigSFUp", "DblMuTrigSFDown"],
               ["JetEnUp", "JetEnDown"],
               ["JetResUp", "JetResDown"],
               ["MuonEnUp", "MuonEnDown"],
               ["HeavyTagUpUnCorr", "HeavyTagDownUnCorr"],
               ["HeavyTagUpCorr", "HeavyTagDownCorr"],
               ["LightTagUpUnCorr", "LightTagDownUnCorr"],
               ["LightTagUpCorr", "LightTagDownCorr"]]

#### get histograms
HISTs = {}
COLORs = {}

## data
fstring = f"{WORKDIR}/data/PromptEstimator/{args.era}/Skim3Mu__{args.network}__/DATA/PromptEstimator_SkimTree_SS2lOR3l_DoubleMuon.root"
# print(fstring)
assert os.path.exists(fstring)
f = ROOT.TFile.Open(fstring)
data = f.Get(f"{args.channel}/Central/{args.key}"); data.SetDirectory(0)
f.Close()

SIGs = {}
# signals
for masspoint in MASSPOINTs:
    fstring =f"{WORKDIR}/data/PromptEstimator/{args.era}/Skim3Mu__{args.network}__ScaleVar__WeightVar__/PromptEstimator_TTToHcToWAToMuMu_{masspoint}.root"
    assert os.path.exists(fstring)
    f = ROOT.TFile.Open(fstring)
    try:
        h = f.Get(f"{args.channel}/Central/{args.key}"); h.SetDirectory(0)
        f.Close()
        SIGs[masspoint] = h.Clone(masspoint); del h
    except Exception as e:
        print(masspoint, e)

# fake
fstring = f"{WORKDIR}/data/MatrixEstimator/{args.era}/Skim3Mu__{args.network}__/DATA/MatrixEstimator_SkimTree_SS2lOR3l_DoubleMuon.root"
assert os.path.exists(fstring)
f = ROOT.TFile.Open(fstring)
fake = f.Get(f"{args.channel}/Central/{args.key}"); fake.SetDirectory(0)
fakeUp = f.Get(f"{args.channel}/NonpromptUp/{args.key}"); fakeUp.SetDirectory(0)
fakeDown = f.Get(f"{args.channel}/NonpromptDown/{args.key}"); fakeDown.SetDirectory(0)
for bin in range(fake.GetNcells()):
    thisError = pow(fake.GetBinError(bin), 2)
    systUp = abs(fakeUp.GetBinContent(bin) - fake.GetBinContent(bin))
    systDown = abs(fakeDown.GetBinContent(bin) - fake.GetBinContent(bin))
    thisError += pow(max(systUp, systDown), 2)
    thisError = sqrt(thisError)
    fake.SetBinError(bin, thisError)
HISTs["nonprompt"] = fake

## Conversion
fstring = f"{WORKDIR}/data/PromptEstimator/{args.era}/Skim3Mu__{args.network}__ScaleVar__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_DYJets.root"
assert os.path.exists(fstring)
f = ROOT.TFile.Open(fstring)
try:
    h = f.Get(f"{args.channel}/Central/{args.key}")
    h.SetDirectory(0)
    hUp = h.Clone("DYJetsUp")
    h.Scale(convSFLowPT[0])
    hUp.Scale(convSFLowPT[0]+convSFLowPT[1])
    for bin in range(h.GetNcells()):
        thisError = pow(h.GetBinError(bin), 2)
        thisSyst = pow(hUp.GetBinContent(bin)-h.GetBinContent(bin), 2)
        thisError = sqrt(thisError)
        h.SetBinError(bin, thisError)
    f.Close()
    HISTs["DYJets"] = h.Clone("DYJets")
except Exception as e:
    print("DYJets", e)


fstring = f"{WORKDIR}/data/PromptEstimator/{args.era}/Skim3Mu__{args.network}__ScaleVar__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_ZGToLLG.root"
assert os.path.exists(fstring)
f = ROOT.TFile.Open(fstring)
try:
    h = f.Get(f"{args.channel}/Central/{args.key}")
    h.SetDirectory(0)
    hUp = h.Clone("ZGToLLGUp")
    h.Scale(convSFHighPT[0])
    hUp.Scale(convSFHighPT[0]+convSFHighPT[1])
    for bin in range(h.GetNcells()):
        thisError = pow(h.GetBinError(bin), 2)
        thisSyst = pow(hUp.GetBinContent(bin)-h.GetBinContent(bin), 2)
        thisError = sqrt(thisError)
        h.SetBinError(bin, thisError)
    f.Close()
    HISTs["ZGToLLG"] = h.Clone("ZGToLLG")
except Exception as e:
    print("ZGToLLG", e)


## prompt
for sample in list(set(MCSamples)-set(CONV)):
    fstring = f"{WORKDIR}/data/PromptEstimator/{args.era}/Skim3Mu__{args.network}__ScaleVar__WeightVar__/PromptEstimator_SkimTree_SS2lOR3l_{sample}.root"
    if not os.path.exists(fstring):
        fstring = f"{WORKDIR}/data/PromptEstimator/{args.era}/Skim3Mu__{args.network}__ScaleVar__WeightVar__/PromptEstimator_{sample}.root"
    try:
        assert os.path.exists(fstring)
        f = ROOT.TFile.Open(fstring)
        h = f.Get(f"{args.channel}/Central/{args.key}")
        h.SetDirectory(0)
        
        # get systematic histograms
        hSysts = []
        for syst in SYSTEMATICs:
            h_up = f.Get(f"{args.channel}/{syst[0]}/{args.key}"); h_up.SetDirectory(0)
            h_down = f.Get(f"{args.channel}/{syst[1]}/{args.key}"); h_down.SetDirectory(0)
            hSysts.append([h_up, h_down])

        for bin in range(h.GetNcells()):
            errInThisBin = [h.GetBinError(bin)]
            for hists in hSysts:
                systUp = abs(h_up.GetBinContent(bin)-h.GetBinContent(bin))
                systDown = abs(h_down.GetBinContent(bin)-h.GetBinContent(bin))
                errInThisBin.append(max(systUp, systDown))
            
            thisError = 0.
            for err in errInThisBin:
                thisError += pow(err, 2)
            thisError = sqrt(err)
            h.SetBinError(bin, thisError)
        f.Close()
        HISTs[sample] = h.Clone(sample)
    except Exception as e:
        print(sample, e)

#### merge backgrounds
def addHist(name, hist, histDict):
    if histDict[name] is None:
        histDict[name] = hist.Clone(name)
    else:
        histDict[name].Add(hist)

temp_dict = {}
temp_dict["nonprompt"] = None
temp_dict["conversion"] = None
temp_dict["ttX"] = None
temp_dict["diboson"] = None
temp_dict["others"] = None

addHist("nonprompt", HISTs['nonprompt'], temp_dict)
for sample in CONV:
    if not sample in HISTs.keys(): continue
    addHist("conversion", HISTs[sample], temp_dict)
for sample in TTX:
    if not sample in HISTs.keys(): continue
    addHist("ttX", HISTs[sample], temp_dict)
for sample in VV:
    if not sample in HISTs.keys(): continue
    addHist("diboson", HISTs[sample], temp_dict)
for sample in RARE:
    if not sample in HISTs.keys(): continue
    addHist("others", HISTs[sample], temp_dict)

#### remove none histogram
BKGs = {}
for key, value in temp_dict.items():
    if temp_dict[key] is None: continue
    BKGs[key] = value

colorList = [ROOT.kBlack, ROOT.kBlue, ROOT.kGray, ROOT.kRed]
for i, masspoint in enumerate(MASSPOINTs):
    COLORs[masspoint] = colorList[i]

COLORs["data"] = ROOT.kBlack
COLORs['nonprompt'] = ROOT.kGray+2
COLORs["ttX"] = ROOT.kBlue
COLORs["conversion"] = ROOT.kViolet
COLORs["diboson"] = ROOT.kGreen
COLORs["others"] = ROOT.kAzure

#### draw plots
if args.blind:
    c = KinematicCanvas(config=config)
    c.drawSignals(SIGs, COLORs)
    c.drawBackgrounds(BKGs, COLORs)
    c.drawLegend()
    c.finalize()
else:
    c = ComparisonCanvas(config=config)
    c.drawBackgrounds(BKGs, COLORs)
    c.drawData(data)
    c.drawRatio()
    c.drawLegend()
    c.finalize()

histpath = f"{WORKDIR}/TriLepRegion/plots/{args.era}/{args.channel}/{args.key.replace('/', '_')}.png"
if not os.path.exists(os.path.dirname(histpath)):
    os.makedirs(os.path.dirname(histpath))
c.savefig(histpath)
