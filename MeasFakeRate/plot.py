import os
import argparse
import ROOT
from math import pow, sqrt
from Plotter import ComparisonCanvas
from histConfigs import histConfigs

#### Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--key", required=True, type=str, help="histkey")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--region", required=True, type=str, help="Inclusive / QCDEnriched / WEnriched / ZEnriched")
parser.add_argument("--id", required=True, type=str, help="loose or tight ID")
args = parser.parse_args()

WORKDIR = os.environ["WORKDIR"]
config = histConfigs[args.key]
config["era"] = args.era

#### Sample list
DataStream = ""
if "El" in args.channel:
    if "2016" in args.era:  DataStream = "DoubleEG"
    if "2017" in args.era:  DataStream = "SingleElectron"
    if "2018" in args.era:  DataStream = "EGamma"
if "Mu" in args.channel:
    DataStream = "DoubleMuon"
    
W  = ["WJets_MG"]
DY = ["DYJets", "DYJets10to50_MG"]
TT = ["TTLL_powheg", "TTLJ_powheg"]
VV = ["WW_pythia", "WZ_pythia", "ZZ_pythia"]
ST = ["SingleTop_sch_Lep", "SingleTop_tch_top_Incl", "SingleTop_tch_antitop_Incl",
      "SingleTop_tW_top_NoFullyHad", "SingleTop_tW_antitop_NoFullyHad"]
MCList = W + DY + TT + VV + ST

#### Systematics
SYSTs = []
if args.channel == "MeasNormEl":
    SYSTs.append(("PileupReweight"))
    SYSTs.append(("L1PrefireUp", "L1PrefireDown"))
    SYSTs.append(("ElectronRecoSFUp", "ElectronRecoSFDown"))
    SYSTs.append(("HeavyTagUpUnCorr", "HeavyTagDownUnCorr"))
    SYSTs.append(("LightTagUpUnCorr", "LightTagDownUnCorr"))
    SYSTs.append(("JetResUp", "JetResDown"))
    SYSTs.append(("JetEnUp", "JetEnDown"))
    SYSTs.append(("ElectronResUp", "ElectronResDown"))
    SYSTs.append(("ElectronEnUp", "ElectronEnDown"))
    SYSTs.append(("MuonEnUp", "MuonEnDown"))
if args.channel == "MeasNormMu":
    SYSTs.append(("PileupReweight"))
    SYSTs.append(("L1PrefireUp", "L1PrefireDown"))
    #SYSTs.append(("MuonRecoSFUp", "MuonRecoSFDown"))
    SYSTs.append(("HeavyTagUpUnCorr", "HeavyTagDownUnCorr"))
    SYSTs.append(("LightTagUpUnCorr", "LightTagDownUnCorr"))
    SYSTs.append(("JetResUp", "JetResDown"))
    SYSTs.append(("JetEnUp", "JetEnDown"))
    SYSTs.append(("ElectronResUp", "ElectronResDown"))
    SYSTs.append(("ElectronEnUp", "ElectronEnDown"))
    SYSTs.append(("MuonEnUp", "MuonEnDown"))

#### Get histograms
HISTs = {}
COLORs = {}

file_path = f"{WORKDIR}/data/MeasFakeRateV3/{args.era}/{args.channel}__/DATA/MeasFakeRateV3_{DataStream}.root"
assert os.path.exists(file_path)
f = ROOT.TFile.Open(file_path)
data = f.Get(f"{args.region}/{args.id}/Central/{args.key}"); data.SetDirectory(0)
f.Close()

for sample in MCList:
    file_path = f"{WORKDIR}/data/MeasFakeRateV3/{args.era}/{args.channel}__RunSyst__/MeasFakeRateV3_{sample}.root"
    assert os.path.exists(file_path)
    # get central histogram
    try:
        f = ROOT.TFile.Open(file_path)
        h = f.Get(f"{args.region}/{args.id}/Central/{args.key}");   h.SetDirectory(0)
        # get systematic histograms
        hSysts = []
        for systset in SYSTs:
            if len(systset) == 2:
                systUp, systDown = systset
                h_up = f.Get(f"{args.region}/{args.id}/{systUp}/{args.key}"); h_up.SetDirectory(0)
                h_down = f.Get(f"{args.region}/{args.id}/{systDown}/{args.key}"); h_down.SetDirectory(0) 
                hSysts.append((h_up, h_down))
            else:
                # only one systematic source
                syst = systset
                h_syst = f.Get(f"{args.region}/{args.id}/{syst}/{args.key}"); h_syst.SetDirectory(0)
                hSysts.append((h_syst))
        f.Close()
    except:
        print(sample)
        continue
    
    # estimate total unc. bin by bin
    for bin in range(h.GetNcells()):
        stat_unc = h.GetBinError(bin)
        envelops = []
        for hset in hSysts:
            if len(hset) == 2:
                h_up, h_down = hset
                systUp = abs(h_up.GetBinContent(bin) - h.GetBinContent(bin))
                systDown = abs(h_up.GetBinContent(bin) - h.GetBinContent(bin))
                envelops.append(max(systUp, systDown))
            else:
                h_syst = hset
                syst = abs(h_syst.GetBinContent(bin) - h.GetBinContent(bin))
                envelops.append(syst)

            total_unc = pow(stat_unc, 2)
            for unc in envelops:
                total_unc += pow(unc, 2)
            total_unc = sqrt(total_unc)
            h.SetBinError(bin, total_unc)
    
    # now central scale
    #h.Scale(0.00045052908036432963)      # mu8 / loose
    h.Scale(0.00044480904623369185)      # mu8 / tight 
    HISTs[sample] = h.Clone(sample)
    
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

hist_path = f"{WORKDIR}/MeasFakeRate/plots/{args.era}/{args.channel}/{args.region}/{args.id}/{args.key.replace('/', '_')}.png"
os.makedirs(os.path.dirname(hist_path), exist_ok=True)
c.savefig(hist_path)

