from histConfigs import hist_configs
from Plotter.comparison import Canvas
from ROOT import kBlack, kGray, kRed, kBlue, kGreen, kMagenta, kCyan, kAzure, kViolet
from ROOT import TFile
from math import pow, sqrt
import argparse
import sys
import os
os.environ['WORKDIR'] = "/home/choij/workspace/ChargedHiggsAnalysis"
sys.path.insert(0, os.environ['WORKDIR'])


# arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", "-e", default=None,
                    required=True, type=str, help="Era")
parser.add_argument("--var", "-v", default=None,
                    required=True, type=str, help="observable")
parser.add_argument("--channel", "-c", default=None,
                    required=True, type=str, help="channel")
#parser.add_argument("--out", "-o", default=None, required=True, type=str, help="output path")
args = parser.parse_args()
config = hist_configs[args.var]

# get histograms
DataStream = "DoubleMuon"
DY = ["DYJets", "DYJets10to50_MG"]
TT = ["TTLL_powheg", "TTLJ_powheg"]
ST = ["SingleTop_sch_Lep",
      "SingleTop_tch_top_Incl",
      "SingleTop_tch_antitop_Incl",
      "SingleTop_tW_top_NoFullyHad",
      "SingleTop_tW_antitop_NoFullyHad"]
VV = ["WW_pythia", "WZ_pythia", "ZZ_pythia"]
MCSamples = DY+TT+ST+VV

Systematics = ["Central",
               ["PileUpCorrUp", "PileUpCorrDown"],
               ["MuonMomentumShiftUp", "MuonMomentumShiftDown"],
               ["JetEnShiftUp", "JetEnShiftDown"],
               ["JetResShiftUp", "JetResShiftDown"],
               ["MuonIDSFUp", "MuonIDSFDown"],
               ["MuonTrigSFUp", "MuonTrigSFDown"]]
# Systematics = ["Default"]
# Systematics = ["MuonIDSFOnly", ["MuonIDSFOnlyUp", "MuonIDSFOnlyDown"]]

f_data = TFile.Open(
    f"SKFlatOutput/{args.era}/DATA/diLepRegion_DoubleMuon.root")
h_data = f_data.Get(f"{args.channel}/Central/{args.var}")
h_data.SetDirectory(0)
f_data.Close()


MCcoll = {}
for mc in MCSamples:
    # get histograms
    central, *systs = Systematics
    f = TFile.Open(f"SKFlatOutput/{args.era}/diLepRegion_{mc}.root")
    h_central = f.Get(f"{args.channel}/{central}/{args.var}")
    if not h_central:
        continue
    h_central.SetDirectory(0)
    h_systs = []
    for syst in systs:
        h_up = f.Get(f"{args.channel}/{syst[0]}/{args.var}")
        h_up.SetDirectory(0)
        h_down = f.Get(f"{args.channel}/{syst[1]}/{args.var}")
        h_down.SetDirectory(0)
        h_systs.append([h_up, h_down])
    f.Close()

    for bin in range(h_central.GetNcells()):
        this_value, this_error = h_central.GetBinContent(
            bin), h_central.GetBinError(bin)
        this_error = pow(this_error, 2)
        for syst in h_systs:
            this_syst_up = syst[0].GetBinContent(bin) - this_value
            this_syst_down = syst[1].GetBinContent(bin) - this_value
            this_syst = this_syst_up if abs(this_syst_up) > abs(
                this_syst_down) else this_syst_down
            this_error += pow(this_syst, 2)
        this_error = sqrt(this_error)
        h_central.SetBinError(bin, this_error)
    MCcoll[mc] = h_central

# Set histogram names
histograms = {}
colors = {}

histograms["data"] = None
colors["data"] = kBlack
histograms["DY"] = None
colors["DY"] = kCyan
histograms["TT"] = None
colors["TT"] = kBlue
histograms["ST"] = None
colors["ST"] = kMagenta
histograms["VV"] = None
colors["VV"] = kGreen


def add_histogram(name, hist, histograms):
    if histograms[name] == None:
        histograms[name] = hist.Clone(name)
    else:
        histograms[name].Add(hist)


add_histogram("data", h_data, histograms)
for sample in DY:
    if not sample in MCcoll.keys():
        continue
    add_histogram("DY", MCcoll[sample], histograms)
for sample in TT:
    if not sample in MCcoll.keys():
        continue
    add_histogram("TT", MCcoll[sample], histograms)
for sample in ST:
    if not sample in MCcoll.keys():
        continue
    add_histogram("ST", MCcoll[sample], histograms)
for sample in VV:
    if not sample in MCcoll.keys():
        continue
    add_histogram("VV", MCcoll[sample], histograms)

# Draw plots
c = Canvas(config=config)
c.draw_distributions(histograms, colors)
c.draw_ratio()
c.draw_legend()
c.draw_latex(args.era)
c.finalize()
c.savefig(
    f"{os.environ['WORKDIR']}/diLepRegion/plots/{args.era}/{args.channel}/{args.var.replace('/', '_')}.png")
