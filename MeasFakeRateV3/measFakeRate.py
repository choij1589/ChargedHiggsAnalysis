#### Measure Fake Rate with systematic variations
#### PromptNorm: 17% for muons, ? for electrons
from math import pow, sqrt
import argparse
import ROOT
ROOT.gSystem.Load("fitFunction_C.so")

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--measure", required=True, type=str, help="muon / electron")
args = parser.parse_args()

#### Samples
DATASTREAM = ""
if args.measure == "muon":
    HLTPATHs = ["MeasFakeMu8", "MeasFakeMu17"]
    DATASTREAM = "DoubleMuon"
elif args.measure == "electron":
    HLTPATHs = ["MeasFakeEl8", "MeasFakeEl12", "MeasFakeEl23"]
    if "2016" in args.era:   DATASTREAM = "DoubleEG"
    elif args.era == "2017": DATASTREAM = "SingleElectron"
    elif args.era == "2018": DATASTREAM = "EGamma"
    else:                    raise KeyError

W = ["WJets_MG"]
DY = ["DYJets", "DYJets10to50_MG"]
TT = ["TTLL_powheg", "TTLJ_powheg"]
VV = ["WW_pythia", "WZ_pythia", "ZZ_pythia"]
ST = ["SingleTop_sch_Lep", "SingleTop_tch_top_Incl", "SingleTop_tch_antitop_Incl",
      "SingleTop_tW_top_NoFullyHad", "SingleTop_tW_antitop_NoFullyHad"]
MC = W+DY+TT+VV+ST

#### Systematics
SYSTs = ["Central",
         "PromptNormUp", "PromptNormDown",
         "MotherJetPtUp", "MotherJetPtDown",
         "RequireHeavyTag",]

def add_mc_hists(samples, hltpath, histkey):
    out = None
    for sample in samples:
        f = ROOT.TFile(f"../data/MeasFakeRateV3/{args.era}/{hltpath}__RunSyst__/MeasFakeRateV3_{sample}.root")
        h = f.Get(histkey)
        if out is None:
            out = h.Clone(f"{sample}_{hltpath}_{id}")
            out.SetDirectory(0)
        else:
            out.Add(h)
        f.Close()
    return out
    

def get_hists(hltpath, id, syst="Central"):
    out = {}
    if syst in ["Central", "PromptNormUp", "PromptNormDown"]:
        histkey = f"Inclusive/{id}/Central/abseta_ptcorr"
    else:
        histkey = f"Inclusive/{id}/{syst}/abseta_ptcorr"
    # get data
    f = ROOT.TFile(f"../data/MeasFakeRateV3/{args.era}/{hltpath}__/DATA/MeasFakeRateV3_{DATASTREAM}.root")
    h = f.Get(histkey.replace(syst, "Central"))
    out["data"] = h.Clone(f"data_{hltpath}_{id}")
    out["data"].SetDirectory(0)
    f.Close()
     
    # get mc
    out["W"] = add_mc_hists(W, hltpath, histkey)
    out["DY"] = add_mc_hists(DY, hltpath, histkey)
    out["TT"] = add_mc_hists(TT, hltpath, histkey)
    out["ST"] = add_mc_hists(ST, hltpath, histkey)
    out["VV"] = add_mc_hists(VV, hltpath, histkey)
    
    ## normalize histograms
    if syst in ["Central", "PromptNormUp", "PromptNormDown"]: 
        fitResult = ROOT.fitMT(args.era, hltpath, id, "Central")
    else:
       fitResult = ROOT.fitMT(args.era, hltpath, id, syst) 
    norm_factors = fitResult.floatParsFinal()
    nevt_data = out["data"].Integral()
    for i in range(norm_factors.getSize()):
        name, value, error = norm_factors.at(i).GetName(), norm_factors.at(i).getVal(), norm_factors.at(i).getError()
        if syst == "PromptNormUp" and args.measure == "muon":
            value *= 1.18
        if syst == "PromptNormDown" and args.measure == "muon":
            value *= 0.82
        #print(name, value, error)
        if "W" in name:  out["W"].Scale(nevt_data/out["W"].Integral()*value)
        if "DY" in name: out["DY"].Scale(nevt_data/out["DY"].Integral()*value)
        if "TT" in name: out["TT"].Scale(nevt_data/out["TT"].Integral()*value)
        if "ST" in name: out["ST"].Scale(nevt_data/out["ST"].Integral()*value)
        if "VV" in name: out["VV"].Scale(nevt_data/out["VV"].Integral()*value)  
    
    return out

if __name__ == "__main__":
    f = ROOT.TFile.Open(f"results/{args.era}/fakerate_{args.measure}.root", "recreate")
    for hltpath in HLTPATHs:
        for syst in SYSTs:
            hists_loose = get_hists(hltpath, "loose", syst)
            hists_tight = get_hists(hltpath, "tight", syst)
            data_loose = hists_loose["data"].Clone(f"data_loose_{hltpath}_{syst}")
            data_tight = hists_tight["data"].Clone(f"data_tight_{hltpath}_{syst}")
            for name in ["W", "DY", "TT", "ST", "VV"]:
                print(f"{name}: {hists_loose[name].Integral()}, {hists_tight[name].Integral()}")
                data_loose.Add(hists_loose[name], -1)
                data_tight.Add(hists_tight[name], -1)
            fr = data_tight.Clone(f"fakerate_{hltpath}_{syst}")
            fr.Divide(data_loose)
            f.cd()
            fr.Write()
    f.Close()



        
        
