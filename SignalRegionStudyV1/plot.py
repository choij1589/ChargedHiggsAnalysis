import os
import argparse
import ROOT
from math import pow, sqrt
from Plotter import KinematicCanvas, ComparisonCanvas
from histConfigs import histConfigs

ROOT.gROOT.SetBatch(True)

#### Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--key", required=True, type=str, help="histkey")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--region", required=True, type=str, help="region")
parser.add_argument("--blind", action="store_true", help="blind mode")
args = parser.parse_args()

WORKDIR = os.environ['WORKDIR']
config = histConfigs[args.key]
config["era"] = args.era
config["yRange"] = [0., 2.]

#### Sample list
DATASTREAM = ""
if "1E2Mu" in args.channel: DATASTREAM = "MuonEG"
if "3Mu" in args.channel: DATASTREAM = "DoubleMuon"
assert DATASTREAM in ["MuonEG", "DoubleMuon"]

CONV = ["DYJets_MG", "DYJets10to50_MG", "TTG", "WWG"]
DIBOSON = ["WZTo3LNu_amcatnlo", "ZZTo4L_powheg"]
TTX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"]
OTHERS = ["WWW", "WWZ", "WZZ", "ZZZ", "tZq", "tHq", "TTTT", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]
MCList = CONV + DIBOSON + TTX + OTHERS

#### Conversion scale factor
ConvSF = {}
if args.era == "2016preVFP":
    ConvSF["Skim1E2Mu"] = (0.850622271153898, 0.046276944570233)
    ConvSF["Skim3Mu"] = (0.644895369602854, 0.133854364953977)
if args.era == "2016postVFP":
    ConvSF["Skim1E2Mu"] = (1.000597462996482, 0.053793736258707)
    ConvSF["Skim3Mu"] = (0.604377666528975, 0.215180026955675)
if args.era == "2017":
    ConvSF["Skim1E2Mu"] = (0.866057016631722, 0.084021568239738)
    ConvSF["Skim3Mu"] = (0.812514384970546, 0.234195906350664)
if args.era == "2018":
    ConvSF["Skim1E2Mu"] = (0.809773290437253, 0.093905182656809)
    ConvSF["Skim3Mu"] = (0.805868730201797, 0.212619914322779)
    
if "MHc" in args.key:
    MASSPOINTs = [args.key.split("/")[0]]
else:
    MASSPOINTs = ["MHc-70_MA-15", "MHc-100_MA-60", "MHc-130_MA-90", "MHc-160_MA-155"]

SYSTs = []
if args.channel == "Skim1E2Mu":
    SYSTs = [("L1PrefireUp", "L1PrefireDown"),
             ("PileupReweightUp", "PileupReweightDown"),
             ("MuonIDSFUp", "MuonIDSFDown"),
             ("ElectronIDSFUp", "ElectronIDSFDown"),
             ("EMuTrigSFUp", "EMuTrigSFDown"),
             ("JetResUp", "JetResDown"),
             ("JetEnUp", "JetEnDown"),
             ("ElectronResUp", "ElectronResDown"),
             ("ElectronEnUp", "ElectronEnDown"),
             ("MuonEnUp", "MuonEnDown"),
             ("HeavyTagUpCorr", "HeavyTagDownCorr"),
             ("HeavyTagUpUnCorr", "HeavyTagDownUnCorr"),
             ("LightTagUpCorr", "LightTagDownCorr"),
             ("LightTagUpUnCorr", "LightTagDownUnCorr")]
if args.channel == "Skim3Mu":
    SYSTs = [("L1PrefireUp", "L1PrefireDown"),
             ("PileupReweightUp", "PileupReweightDown"),
             ("MuonIDSFUp", "MuonIDSFDown"),
             ("DblMuTrigSFUp", "DblMuTrigSFDown"),
             ("JetResUp", "JetResDown"),
             ("JetEnUp", "JetEnDown"),
             ("MuonEnUp", "MuonEnDown"),
             ("HeavyTagUpCorr", "HeavyTagDownCorr"),
             ("HeavyTagUpUnCorr", "HeavyTagDownUnCorr"),
             ("LightTagUpCorr", "LightTagDownCorr"),
             ("LightTagUpUnCorr", "LightTagDownUnCorr")]

#### get histograms
HISTs = {}
COLORs = {}

## data
file_path = f"{WORKDIR}/data/PromptEstimator/{args.era}/{args.channel}__/DATA/PromptEstimator_SkimTree_SS2lOR3l_{DATASTREAM}.root"
assert os.path.exists(file_path)
f = ROOT.TFile.Open(file_path)
data = f.Get(f"{args.region}/Central/{args.key}"); data.SetDirectory(0)
f.Close()

SIGs = {}
# signals
for masspoint in MASSPOINTs:
    file_path =f"{WORKDIR}/data/PromptEstimator/{args.era}/{args.channel}__RunSyst__/PromptEstimator_TTToHcToWAToMuMu_{masspoint}.root"
    assert os.path.exists(file_path)
    f = ROOT.TFile.Open(file_path)
    h = f.Get(f"{args.region}/Central/{args.key}"); h.SetDirectory(0)
    f.Close()
    SIGs[masspoint] = h.Clone(masspoint)


## nonprompt
file_path = f"{WORKDIR}/data/MatrixEstimator/{args.era}/{args.channel}__/DATA/MatrixEstimator_SkimTree_SS2lOR3l_{DATASTREAM}.root"
assert os.path.exists(file_path)
f = ROOT.TFile.Open(file_path)
h = f.Get(f"{args.region}/Central/{args.key}"); h.SetDirectory(0)
f.Close()

for bin in range(h.GetNcells()):
    h.SetBinError(bin, h.GetBinContent(bin)*0.3)
HISTs["nonprompt"] = h.Clone("nonprompt")

for sample in MCList:
    file_path = f"{WORKDIR}/data/PromptEstimator/{args.era}/{args.channel}__RunSyst__/PromptEstimator_SkimTree_SS2lOR3l_{sample}.root"
    assert os.path.exists(file_path)
    f = ROOT.TFile.Open(file_path)
    h = f.Get(f"{args.region}/Central/{args.key}")
    
    try:
        h.SetDirectory(0)
    except Exception as e:
        print(sample, e)
        f.Close()
        continue
    
    if sample in CONV:
        convsf, converr = ConvSF[args.channel] 
        h.Scale(convsf)
        for bin in range(h.GetNcells()):
            h.SetBinError(bin, h.GetBinContent(bin)*(converr/convsf))
    else:
        hSysts = []
        for systUp, systDown in SYSTs:
            h_up = f.Get(f"{args.region}/{systUp}/{args.key}"); h_up.SetDirectory(0)
            h_down = f.Get(f"{args.region}/{systDown}/{args.key}"); h_down.SetDirectory(0)
            hSysts.append((h_up, h_down))
        
        # estimate total unc. bin by bin 
        for bin in range(h.GetNcells()):
            stat_unc = h.GetBinError(bin)
            envelops = []
            for h_up, h_down in hSysts:
                systUp = abs(h_up.GetBinContent(bin) - h.GetBinContent(bin))
                systDown = abs(h_up.GetBinContent(bin) - h.GetBinContent(bin))
                envelops.append(max(systUp, systDown))
    
            total_unc = pow(stat_unc, 2)
            for unc in envelops:
                total_unc += pow(unc, 2)
            total_unc = sqrt(total_unc)
            h.SetBinError(bin, total_unc)
    f.Close()
    HISTs[sample] = h.Clone(sample)
    
#### merge backgrounds
def add_hist(name, hist, histDict):
    # content of dictionary should be initialized as "None"
    if histDict[name] is None:
        histDict[name] = hist.Clone(name)
    else:
        histDict[name].Add(hist)
        
temp_dict = {}
temp_dict["nonprompt"] = HISTs["nonprompt"]
temp_dict["conversion"]  = None
temp_dict["diboson"] = None
temp_dict["tt+W/Z/H"] = None
temp_dict["others"] = None 

temp_dict = {}
temp_dict["nonprompt"] = HISTs["nonprompt"]
temp_dict["conversion"]  = None
temp_dict["diboson"] = None
temp_dict["tt+W/Z/H"] = None
temp_dict["others"] = None 

for sample in CONV:
    if not sample in HISTs.keys(): continue
    add_hist("conversion", HISTs[sample], temp_dict)
for sample in DIBOSON:
    if not sample in HISTs.keys(): continue
    add_hist("diboson", HISTs[sample], temp_dict)
for sample in TTX:
    if not sample in HISTs.keys(): continue
    add_hist("tt+W/Z/H", HISTs[sample], temp_dict)
for sample in OTHERS:
    if not sample in HISTs.keys(): continue
    add_hist("others", HISTs[sample], temp_dict)
    
#### remove none histograms
BKGs = {}
for key, value in temp_dict.items():
    if value is None: continue
    BKGs[key] = value

colorList = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kInvertedDarkBodyRadiator]

for i, masspoint in enumerate(MASSPOINTs):
    COLORs[masspoint] = colorList[i]
 
COLORs["data"] = ROOT.kBlack
COLORs["nonprompt"] = ROOT.kGray
COLORs["conversion"] = ROOT.kViolet
COLORs["diboson"] = ROOT.kGreen
COLORs["tt+W/Z/H"] = ROOT.kBlue
COLORs["others"] = ROOT.kYellow

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

hist_path = f"{WORKDIR}/SignalRegionStudyV1/plots/{args.era}/{args.channel}/{args.region}/{args.key.replace('/', '_')}.png"
os.makedirs(os.path.dirname(hist_path), exist_ok=True)
c.savefig(hist_path)
