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
parser.add_argument("--hltpath", required=True, type=str, help="HLT trigger path")
args = parser.parse_args()

WORKDIR = os.environ["WORKDIR"]
config = histConfigs[args.key]
config["era"] = args.era

#### check arguments
if not args.era in ["2016preVFP", "2016postVFP", "2017", "2018"]:
    print(f"Wrong era {args.era}")
    raise(KeyError)
if not args.channel in ["MeasNormEl", "MeasNormMu", "MeasFakeEl", "MeasFakeMu"]:
    print(f"Wrong channel {args.channel}")
    raise(KeyError)

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
    SYSTs.append(("MuonRecoSFUp", "MuonRecoSFDown"))
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

file_path = f"{WORKDIR}/data/MeasFakeRate/{args.era}/{args.channel}__/DATA/MeasFakeRate_{DataStream}.root"
assert os.path.exists(file_path)
f = ROOT.TFile.Open(file_path)
data = f.Get(f"{args.channel}/Central/{args.key}");









