import os
import argparse
import ROOT
from math import pow, sqrt
from Plotter import ComparisonCanvas
from histConfigs import histConfigs

#### Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--noSF", action="store_true", default=False, help="remove lepton scale factors")
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--key", required=True, type=str, help="histkey")
parser.add_argument("--channel", required=True, type=str, help="channel")
args = parser.parse_args()

WORKDIR = os.environ["WORKDIR"]
config = histConfigs[args.key]
config["era"] = args.era

#### Sample list
DataStream = ""

W  = ["WJets_MG"]
DY = ["DYJets", "DYJets10to50_MG"]
TT = ["TTLL_powheg", "TTLJ_powheg"]
VV = ["WW_pythia", "WZ_pythia", "ZZ_pythia"]
ST = ["SingleTop_sch_Lep", "SingleTop_tch_top_Incl", "SingleTop_tch_antitop_Incl",
      "SingleTop_tW_top_NoFullyHad", "SingleTop_tW_antitop_NoFullyHad"]
MCList = W + DY + TT + VV + ST

#### Systematics
if args.channel == "DiMu":
    DataStream = "DoubleMuon"
    SYSTs = [("L1PrefireUp", "L1PrefireDown"),
             ("PileupReweightUp", "PileupReweightDown"),
             ("MuonIDSFUp", "MuonIDSFDown"),
             ("DblMuTrigSFUp", "DblMuTrigSFDown"),
             ("MuonEnUp", "MuonEnDown"),
             ("ElectronEnUp", "ElectronEnDown"),
             ("ElectronResUp", "ElectronResDown"),
             ("JetEnUp", "JetEnDown"),
             ("JetResUp", "JetResDown")]
elif args.channel == "EMu":
    DataStream = "MuonEG"
    SYSTs = [("L1PrefireUp", "L1PrefireDown"),
             ("PileupReweightUp", "PileupReweightDown"),
             ("MuonIDSFUp", "MuonIDSFDown"),
             ("ElectronIDSFUp", "ElectronIDSFDown"),
             ("EMuTrigSFUp", "EMuTrigSFDown"),
             ("HeavyTagUpUnCorr", "HeavyTagDownUnCorr"),
             ("HeavyTagUpCorr", "HeavyTagDownCorr"),
             ("LightTagUpUnCorr", "LightTagDownUnCorr"),
             ("LightTagUpCorr", "LightTagDownCorr"),
             ("MuonEnUp", "MuonEnDown"),
             ("ElectronEnUp", "ElectronEnDown"),
             ("ElectronResUp", "ElectronResDown"),
             ("JetEnUp", "JetEnDown"),
             ("JetResUp", "JetResDown")]


#### Get histograms
HISTs = {}
COLORs = {}

file_path = f"{WORKDIR}/data/DiLeptonValidation/{args.era}/Run{args.channel}__/DATA/DiLeptonValidation_{DataStream}.root"
assert os.path.exists(file_path)
f = ROOT.TFile.Open(file_path)
data = f.Get(f"{args.channel}/Central/{args.key}"); data.SetDirectory(0)
f.Close()

for sample in MCList:
    file_path = f"{WORKDIR}/data/DiLeptonValidation/{args.era}/Run{args.channel}__RunSyst__/DiLeptonValidation_{sample}.root" 
    #file_path = f"{WORKDIR}/data/DiLeptonValidation/{args.era}/Run{args.channel}__/DiLeptonValidation_{sample}.root" 
    #print(file_path)
    assert os.path.exists(file_path)
    f = ROOT.TFile.Open(file_path)
    try:
        if args.noSF:
            h = f.Get(f"{args.channel}/Central_NoLeptonWeight/{args.key}"); h.SetDirectory(0)
            f.Close()
        else:
            h = f.Get(f"{args.channel}/Central/{args.key}"); h.SetDirectory(0)
            # get systematic histograms
            hSysts = []
            for systUp, systDown in SYSTs:
                h_up = f.Get(f"{args.channel}/{systUp}/{args.key}"); h_up.SetDirectory(0)
                h_down = f.Get(f"{args.channel}/{systDown}/{args.key}"); h_down.SetDirectory(0)
                hSysts.append((h_up, h_down))
            f.Close()
        
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
        HISTs[sample] = h.Clone(sample)
    except Exception as e:
        print(sample, e)
    
#### merge backgrounds
def add_hist(name, hist, histDict):
    # content of dictionary should be initialized as "None"
    if histDict[name] is None:
        histDict[name] = hist.Clone(name)
    else:
        histDict[name].Add(hist)
    
temp_dict = {}
temp_dict["W"]  = None
temp_dict["DY"] = None
temp_dict["TT"] = None
temp_dict["VV"] = None 
temp_dict["ST"] = None

for sample in W:
    if not sample in HISTs.keys(): continue
    add_hist("W", HISTs[sample], temp_dict)
for sample in DY:
    if not sample in HISTs.keys(): continue
    add_hist("DY", HISTs[sample], temp_dict)
for sample in TT:
    if not sample in HISTs.keys(): continue
    add_hist("TT", HISTs[sample], temp_dict)
for sample in VV:
    if not sample in HISTs.keys(): continue
    add_hist("VV", HISTs[sample], temp_dict)
for sample in ST:
    if not sample in HISTs.keys(): continue
    add_hist("ST", HISTs[sample], temp_dict)
    
#### remove none histograms
BKGs = {}
for key, value in temp_dict.items():
    if value is None: continue
    BKGs[key] = value

COLORs["data"] = ROOT.kBlack
COLORs["W"]  = ROOT.kMagenta
COLORs["DY"] = ROOT.kGray
COLORs["TT"] = ROOT.kViolet
COLORs["VV"] = ROOT.kGreen
COLORs["ST"] = ROOT.kAzure

#### draw plots
c = ComparisonCanvas(config=config)
c.drawBackgrounds(BKGs, COLORs)
c.drawData(data)
c.drawRatio()
c.drawLegend()
c.finalize()

if args.noSF:
    hist_path = f"{WORKDIR}/DiLeptonValidation/plots/{args.era}/{args.channel}/noLeptonSF/{args.key.replace('/', '_')}.png"
else:
    hist_path = f"{WORKDIR}/DiLeptonValidation/plots/{args.era}/{args.channel}/{args.key.replace('/', '_')}.png"
os.makedirs(os.path.dirname(hist_path), exist_ok=True)
c.savefig(hist_path)
