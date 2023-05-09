import os, shutil
import argparse
import ROOT
import pandas as pd
from ConvScaleFactors import ConvSF

WORKDIR = os.getenv("WORKDIR")
ROOT.gSystem.Load(f"{WORKDIR}/libCpp/prepareDatacard_cc.so")
ROOT.EnableImplicitMT(8)

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--network", required=True, type=str, help="network")
parser.add_argument("--sampleKey", required=True, type=str, help="sample key for group of samples")
parser.add_argument("--doCnC", action="store_true", default=False, help="do CnC or shape")
parser.add_argument("--doCut", action="store_true", default=False, help="use optimized score cuts?")
args = parser.parse_args()

# conversion scale factors
convsf = ConvSF[args.era[:4]]
convsf_lowpt = ROOT.std.pair[ROOT.double, ROOT.double]()
convsf_lowpt.first, convsf_lowpt.second = tuple(convsf["LowPT3Mu"])
convsf_highpt = ROOT.std.pair[ROOT.double, ROOT.double]()
convsf_highpt.first, convsf_highpt.second = tuple(convsf["HighPT3Mu"])

# scores
scores = ROOT.std.pair[ROOT.double, ROOT.double]()
if args.doCut:
    csvPath = f"{WORKDIR}/SignalRegionStudy/{args.era}/{args.channel}__{args.network}__/{args.signal}/result.csv"
    csv = pd.read_csv(csvPath, header=None)
    scores.first = csv.iloc[0, 2]
    scores.second = csv.iloc[0, 3]
else:
    scores.first = 0.
    scores.second = 0.

# systemtic lists
systsWithSampleKey = {
        "prompt": ["Central", "MuonIDSFUp", "MuonIDSFDown", "DblMuTrigSFUp", "DblMuTrigSFDown",
                              "JetEnUp", "JetEnDown", "JetResUp", "JetResDown"],
        "nonprompt": ["Central", "NonpromptUp", "NonpromptDown"],
        "conversion": ["Central", "ConversionUp", "ConversionDown"]
        }

outPath = f"{WORKDIR}/SignalRegionStudy/{args.era}/{args.channel}__{args.network}__/{args.signal}/datacard.input.{args.sampleKey}"
if args.doCnC: outPath = f"{outPath}.CnC"
else:          outPath = f"{outPath}.shape"

if args.doCut: outPath = f"{outPath}.withcut.root"
else:          outPath = f"{outPath}.nocut.root"

print(f"[prepareDatacard] outpath = {outPath}")

f = ROOT.TFile(outPath, "recreate")
if args.sampleKey == "nonprompt":
    systematics = systsWithSampleKey["nonprompt"]
elif args.sampleKey == "conversion":
    systematics = systsWithSampleKey["conversion"]
else:
    systematics = systsWithSampleKey["prompt"]

for syst in systematics:
    if args.signal == args.sampleKey:
        filePath = f"{WORKDIR}/data/PromptUnbinned/{args.era}/{args.channel}__{args.network}__/PromptUnbinned_TTToHcToWAToMuMu_{args.signal}.root"
        h = ROOT.makeHisto1DSingle(filePath, args.signal, args.sampleKey, scores, convsf_lowpt, convsf_highpt, syst)
    else:
        h = ROOT.makeHisto1D(args.era, args.channel, args.signal, args.network, args.sampleKey, scores, convsf_lowpt, convsf_highpt, syst)
    h.SetDirectory(0)
    f.cd()
    h.Write()
f.Close()
