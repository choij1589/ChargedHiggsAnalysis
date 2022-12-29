import os, sys
sys.path.insert(0, os.environ['WORKDIR'])
import argparse

from math import pow, sqrt
from ROOT import kBlack, kYellow, kGray, kRed, kBlue, kGreen, kMagenta, kCyan, kAzure, kViolet
from ROOT import TFile
from libPython.DataDriven import Conversion
from histConfig import hist_configs

# Agruments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--var", required=True, type=str, help="observable")
parser.add_argument("--region", required=True, type=str, help="SignalRegion/ZFakeRegion/ZGammaRegion")
args = parser.parse_args()

DataStream = "DoubleMuon"
Conv = ["DYJets", "ZGToLLG"]
VV = ["WZTo3LNu_amcatnlo", "ZZTo4L_powheg"]
ttX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb", "tZq", "tHq"]
Rare = ["WWW", "WWZ", "WZZ", "ZZZ", "WWG", "TTG", "TTTT", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]
MCSamples = Conv + VV + ttX + Rare

MASSPOINTs = []
BLIND = False
if args.region == "SignalRegion":
    MASSPOINTs = ["MHc-70_MA-15", "MHc-100_MA-60", "MHc-130_MA-90", "MHc-160_MA-155"] 
    BLIND = True

Systematics = ["Central",
               ["L1PrefireUp", "L1PrefireDown"],
               ["PileUpCorrUp", "PileUpCorrDown"],
               ["MuonMomentumShiftUp", "MuonMomentumShiftDown"],
               ["JetEnShiftUp", "JetEnShiftDown"],
               ["JetResShiftUp", "JetResShiftDown"],
               ["MuonIDSFUp", "MuonIDSFDown"],
               ["DblMuonTrigSFUp", "DblMuonTrigSFDown"]
               ]

# get histograms
# data
f = TFile.Open(f"ROOT/Skim3Mu__/{args.era}/{DataStream}.root")
h_data = f.Get(f"3Mu/{args.region}/Central/Incl/{args.var}")
h_data.SetDirectory(0)
h_fake = f.Get(f"3Mu/{args.region}/Nonprompt/Incl/{args.var}")
h_fake.SetDirectory(0)
h_fake_up = f.Get(f"3Mu/{args.region}/NonpromptUp/Incl/{args.var}")
h_fake_up.SetDirectory(0)
h_fake_down = f.Get(f"3Mu/{args.region}/NonpromptDown/Incl/{args.var}")
h_fake_down.SetDirectory(0)
f.Close()

for bin in range(h_fake.GetNcells()):
    this_value, this_error = h_fake.GetBinContent(bin), h_fake.GetBinError(bin)
    this_error = pow(this_error, 2)
    this_syst_up = h_fake_up.GetBinContent(bin) - this_value
    this_syst_down = h_fake_down.GetBinContent(bin) - this_value
    this_syst = max(abs(this_syst_up), abs(this_syst_down))
    this_error += pow(this_syst, 2)
    this_error = sqrt(this_error)
    h_fake.SetBinError(bin, this_error)

# Signals
signals = {}
for masspoint in MASSPOINTs:
    f = TFile.Open(f"ROOT/Skim3Mu__/{args.era}/TTToHcToWAToMuMu_{masspoint}.root")
    h = f.Get(f"3Mu/{args.region}/Central/Incl/{args.var}")
    h.SetDirectory(0)
    f.Close()
    signals[masspoint] = h.Clone(masspoint)
    del h

# MC Backgrounds
MCcoll = {}
ConvSF = Conversion(era=args.era)
for sample in MCSamples:
    if sample not in Conv:
        central, *systs = Systematics
        f = TFile.Open(f"ROOT/Skim3Mu__/{args.era}/{sample}.root")
        h_cent = f.Get(f"3Mu/{args.region}/Central/Incl/{args.var}")
        if not h_cent:
            continue
        h_cent.SetDirectory(0)
        h_systs = []
        for syst in systs:
            h_up = f.Get(f"3Mu/{args.region}/{syst[0]}/Incl/{args.var}")
            h_up.SetDirectory(0)
            h_down = f.Get(f"3Mu/{args.region}/{syst[1]}/Incl/{args.var}")
            h_down.SetDirectory(0)
            h_systs.append([h_up, h_down])
        f.Close()

        for bin in range(h_cent.GetNcells()):
            this_value, this_error = h_cent.GetBinContent(bin), h_cent.GetBinError(bin)
            this_error = pow(this_error, 2)
            for syst in h_systs:
                this_syst_up = syst[0].GetBinContent(bin) - this_value
                this_syst_down = syst[1].GetBinContent(bin) - this_value
                this_syst = max(abs(this_syst_up), abs(this_syst_down))
                this_error += pow(this_syst, 2)
            this_error = sqrt(this_error)
            h_cent.SetBinError(bin, this_error)
    else:
        measure = "DYJets" if sample == "DYJets" else "ZGamma"
        f = TFile.Open(f"ROOT/Skim3Mu__/{args.era}/{sample}.root")
        h_cent = f.Get(f"3Mu/{args.region}/Central/{measure}/{args.var}")
        if not h_cent: continue
        h_cent.SetDirectory(0)
        h_up = h_cent.Clone("conv_up")
        h_down = h_cent.Clone("conv_down")
        
        # scale and set systematics
        h_cent.Scale(ConvSF.getScale(measure))
        h_up.Scale(ConvSF.getScale(measure, 1))
        h_down.Scale(ConvSF.getScale(measure, -1))
        for bin in range(h_cent.GetNcells()):
            this_value = h_cent.GetBinContent(bin)
            this_syst_up = h_up.GetBinContent(bin) - this_value
            this_syst_down = h_down.GetBinContent(bin) - this_value
            this_syst = max(abs(this_syst_up), abs(this_syst_down))
            h_cent.SetBinError(bin, this_syst)
    if sample == "ZZTo4L_powheg":
        h_cent.Scale(186./19.)
    MCcoll[sample] = h_cent


# Set histogram names
histograms = {}
colors = {}
histograms['data'] = None
histograms['fake'] = None
histograms['conv'] = None
histograms['VV'] = None
histograms['ttX'] = None
histograms['rare'] = None

def add_histogram(name, hist, histograms):
    # first clone or add histogram
    if histograms[name] == None:
        histograms[name] = hist.Clone(name)
    else:
        histograms[name].Add(hist)


add_histogram("data", h_data, histograms)
add_histogram("fake", h_fake, histograms)
for sample in Conv:
    if not sample in MCcoll.keys():
        continue
    add_histogram("conv", MCcoll[sample], histograms)
for sample in VV:
    if not sample in MCcoll.keys():
        continue
    add_histogram("VV", MCcoll[sample], histograms)
for sample in ttX:
    if not sample in MCcoll.keys():
        continue
    add_histogram("ttX", MCcoll[sample], histograms)
for sample in Rare:
    if not sample in MCcoll.keys():
        continue
    add_histogram("rare", MCcoll[sample], histograms)

# colors
colors['data'] = kBlack
colors['fake'] = kGray
colors['conv'] = kCyan
colors['VV'] = kGreen
colors['ttX'] = kBlue
colors['rare'] = kRed

colorList = [kRed, kGreen, kGray, kCyan]
for i, masspoint in enumerate(MASSPOINTs):
    colors[masspoint] = colorList[i]

# Draw plots
config = hist_configs[args.var]
config['ratio'] = [0., 2.]

if BLIND:
    from plotter.kinematics import Canvas
    histograms.pop("data")
    c = Canvas(config=config)
    c.draw_signals(signals, colors)
    c.draw_backgrounds(histograms, colors)
    c.draw_legend()
    c.finalize(args.era)
    c.savefig(f"./plots/{args.era}/{args.region}/{args.var.replace('/', '_')}.png")
else:
    from plotter.comparison import Canvas
    c = Canvas(config=config)
    c.draw_distributions(histograms, colors)
    c.draw_ratio()
    c.draw_legend()
    c.finalize(args.era)
    c.savefig(f"./plots/{args.era}/{args.region}/{args.var.replace('/', '_')}.png")
