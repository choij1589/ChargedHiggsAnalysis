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
args = parser.parse_args()

WORKDIR = os.environ['WORKDIR']
config = histConfigs[args.key]
config["era"] = args.era

#### Sample list
DataStream = ""
if "EMu" in args.channel: DataStream = "MuonEG"
if "DiMu" in args.channel: DataStream = "DoubleMuon"

W  = ["WJets_MG"]
DY = ["DYJets", "DYJets10to50_MG"]
TTLL = ["TTLL_powheg"]
TTLJ = ["TTLJ_powheg"]
VV = ["WW_pythia", "WZ_pythia", "ZZ_pythia"]
ST = ["SingleTop_sch_Lep", "SingleTop_tch_top_Incl", "SingleTop_tch_antitop_Incl", 
      "SingleTop_tW_top_NoFullyHad", "SingleTop_tW_antitop_NoFullyHad"]
MCSamples = W + DY + TTLL + TTLJ + VV + ST

#### Systematics
SYSTEMATICs = [["L1PrefireUp", "L1PrefireDown"],
               ["PileupReweightUp", "PileupReweightDown"],
               ["MuonIDSFUp", "MuonIDSFDown"],
               ["DblMuTrigSFUp", "DblMuTrigSFDown"]]

#### get histograms
HISTs = {}
COLORs = {}

fstring = f"{WORKDIR}/data/CR_DiLepton/{args.era}/DATA/CR_DiLepton_DoubleMuon.root"
assert os.path.exists(fstring)
f = ROOT.TFile.Open(fstring)
data = f.Get(f"{args.channel}/Central/{args.key}")
data.SetDirectory(0)
f.Close()

for sample in MCSamples:
    fstring = f"{WORKDIR}/data/CR_DiLepton/{args.era}/RunSyst__/CR_DiLepton_{sample}.root"
    assert os.path.exists(fstring)
    f = ROOT.TFile.Open(fstring)
    try:
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
temp_dict["W"] = None
temp_dict["DY"] = None
temp_dict["TTLL"] = None
temp_dict["TTLJ"] = None
temp_dict["VV"] = None
temp_dict["ST"] = None

for sample in W:
    if not sample in HISTs.keys(): continue
    addHist("W", HISTs[sample], temp_dict)
for sample in DY:
    if not sample in HISTs.keys(): continue
    addHist("DY", HISTs[sample], temp_dict)
for sample in TTLL:
    if not sample in HISTs.keys(): continue
    addHist("TTLL", HISTs[sample], temp_dict)
for sample in TTLJ:
    if not sample in HISTs.keys(): continue
    addHist("TTLJ", HISTs[sample], temp_dict)
for sample in VV:
    if not sample in HISTs.keys(): continue
    addHist("VV", HISTs[sample], temp_dict)
for sample in ST:
    if not sample in HISTs.keys(): continue
    addHist("ST", HISTs[sample], temp_dict) 

#### remove none histogram
BKGs = {}
for key, value in temp_dict.items():
    if temp_dict[key] is None: continue
    BKGs[key] = value



COLORs["data"] = ROOT.kBlack
COLORs["W"]  = ROOT.kRed
COLORs["DY"] = ROOT.kMagenta
COLORs["TTLL"] = ROOT.kBlue
COLORs["TTLJ"] = ROOT.kViolet
COLORs["VV"] = ROOT.kGreen
COLORs["ST"] = ROOT.kAzure

#### draw plots
c = ComparisonCanvas(config=config)
c.drawBackgrounds(BKGs, COLORs)
c.drawData(data)
c.drawRatio()
c.drawLegend()
c.finalize()

histpath = f"{WORKDIR}/DiLeptonRegion/plots/{args.era}/{args.channel}/{args.key.replace('/', '_')}.png"
if not os.path.exists(os.path.dirname(histpath)):
    os.makedirs(os.path.dirname(histpath))
c.savefig(histpath)

    
    
    
    
    
    
    
