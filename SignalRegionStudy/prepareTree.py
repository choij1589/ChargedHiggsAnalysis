import os, shutil
import argparse
import ROOT

WORKDIR = os.getenv("WORKDIR")
ROOT.gSystem.Load(f"{WORKDIR}/libCpp/prepareTree_cc.so")
ROOT.EnableImplicitMT(4)

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--sample", required=True, type=str, help="sample name")
args = parser.parse_args()

Systematics = {
        "prompt": ["Central", "MuonIDSFUp", "MuonIDSFDown", "DblMuTrigSFUp", "DblMuTrigSFDown",
                              "JetEnUp", "JetEnDown", "JetResUp", "JetResDown"],
        "nonprompt": ["Central", "NonpromptUp", "NonpromptDown"]
}


#### make file path
nonSkim = ["TTTT", "WWG", "tHq"]
# signal sample
if args.sample == args.signal:
    filepath = f"{WORKDIR}/data/PromptUnbinned/{args.era}/{args.channel}__DenseNet__/PromptUnbinned_TTToHcToWAToMuMu_{args.sample}.root"
elif args.sample == "nonprompt":
    filepath = f"{WORKDIR}/data/MatrixUnbinned/{args.era}/{args.channel}__DenseNet__/DATA/MatrixUnbinned_SkimTree_SS2lOR3l_DoubleMuon.root"
elif args.sample in nonSkim:
    filepath = f"{WORKDIR}/data/PromptUnbinned/{args.era}/{args.channel}__DenseNet__/PromptUnbinned_{args.sample}.root"
else:
    filepath = f"{WORKDIR}/data/PromptUnbinned/{args.era}/{args.channel}__DenseNet__/PromptUnbinned_SkimTree_SS2lOR3l_{args.sample}.root"

outpath = f"{WORKDIR}/SignalRegionStudy/Parametric/{args.era}/{args.channel}__/{args.signal}/{args.sample}.root"
if not os.path.exists(os.path.dirname(outpath)):
    os.makedirs(os.path.dirname(outpath))
out = ROOT.TFile(outpath, "recreate")

MA = float(args.signal.split("_")[1].split("-")[1])
systs = Systematics["nonprompt"] if args.sample == "nonprompt" else Systematics["prompt"]
for syst in systs:
    tree = ROOT.prepareDataset(filepath, args.sample, MA, syst)
    out.cd()
    tree.Write()
out.Close()
