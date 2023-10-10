import os
import argparse 
import ROOT
import pandas as pd
from ctypes import c_double
from itertools import product

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--measure", required=True, type=str, help="electron / muon")
args = parser.parse_args()

#### Settings
WORKDIR = os.environ["WORKDIR"]
DataStream = ""
ptCorr_bins = []
abseta_bins = []
SYSTs = []

if args.measure == "electron":
    if "2016" in args.era:  DataStream = "DoubleEG"
    if "2017" in args.era:  DataStream = "SingleElectron"
    if "2018" in args.era:  DataStream = "EGamma"
    ptCorr_bins = [10., 15., 20., 25., 35., 50., 100.]
    abseta_bins = [0., 0.8, 1.479, 2.5]
    QCD = ["QCD_EMEnriched", "QCD_bcToE"]
    #QCD = ["QCD"]
    SYSTs = ["Central", "Stat",
             "PileupReweight",
             "L1PrefireUp", "L1PrefireDown",
             "ElectronRecoSFUp", "ElectronRecoSFDown",
             "JetResUp", "JetResDown",
             "JetEnUp", "JetEnDown",
             "ElectronResUp", "ElectronResDown",
             "ElectronEnUp", "ElectronEnDown",
             "MuonEnUp", "MuonEnDown",
             "MotherJetPtUp", "MotherJetPtDown",
             "RequireHeavyTag"]
elif args.measure == "muon":
    DataStream = "DoubleMuon"
    ptCorr_bins = [10., 15., 20., 30., 50., 100.]
    abseta_bins = [0., 0.9, 1.6, 2.4]
    QCD = ["QCD_MuEnriched"]
    SYSTs = ["Central", "Stat",
             "PileupReweight",
             "L1PrefireUp", "L1PrefireDown",
             "MuonRecoSFUp", "MuonRecoSFDown",
             "JetResUp", "JetResDown",
             "JetEnUp", "JetEnDown",
             "ElectronResUp", "ElectronResDown",
             "ElectronEnUp", "ElectronEnDown",
             "MuonEnUp", "MuonEnDown",
             "MotherJetPtUp", "MotherJetPtDown",
             "RequireHeavyTag"]
else:
    raise KeyError(f"Wrong measure {args.measure}")

W  = ["WJets_MG"]
DY = ["DYJets", "DYJets10to50_MG"]
TT = ["TTLL_powheg", "TTLJ_powheg"]
VV = ["WW_pythia", "WZ_pythia", "ZZ_pythia"]
ST = ["SingleTop_sch_Lep", "SingleTop_tch_top_Incl", "SingleTop_tch_antitop_Incl",
      "SingleTop_tW_top_NoFullyHad", "SingleTop_tW_antitop_NoFullyHad"]
MCList = W + DY + TT + VV + ST + QCD

def findbin(ptCorr, abseta):
    if ptCorr > 100.:
        #print(f"ptCorr = {ptCorr}")
        ptCorr = 99.

    prefix = ""
    # find bin index for ptcorr
    for i in range(len(ptCorr_bins)-1):
        if ptCorr_bins[i] < ptCorr+1e-5 < ptCorr_bins[i+1]:
            prefix += f"ptCorr_{int(ptCorr_bins[i])}to{int(ptCorr_bins[i+1])}"
            break
    # find bin index for abseta
    for i in range(len(abseta_bins)-1):
        if abseta_bins[i] < abseta+1e-5 < abseta_bins[i+1]:
            prefix += f"_abseta_{str(abseta_bins[i]).replace('.', 'p')}to{str(abseta_bins[i+1]).replace('.', 'p')}"
    return prefix

def get_hist(sample, ptCorr, abseta, id, syst="Central"):
    prefix = findbin(ptCorr, abseta) 
    channel = ""
    if args.measure == "muon":
        if ptCorr < 30.: channel = "MeasFakeMu8"
        else:            channel = "MeasFakeMu17"
    if args.measure == "electron":
        if   ptCorr < 20.: channel = "MeasFakeEl8"
        elif ptCorr < 35.: channel = "MeasFakeEl12"
        else:              channel = "MeasFakeEl23"
    file_path = ""
    if sample == DataStream:
        file_path = f"{WORKDIR}/data/MeasFakeRateV4/{args.era}/{channel}__RunSyst__/DATA/MeasFakeRateV4_{sample}.root"
    elif "QCD" in sample:
        file_path = f"{WORKDIR}/data/MeasFakeRateV4/{args.era}/{channel}__/MeasFakeRateV4_{sample}.root"
    else:
        file_path = f"{WORKDIR}/data/MeasFakeRateV4/{args.era}/{channel}__RunSyst__/MeasFakeRateV4_{sample}.root"
    try:
        assert os.path.exists(file_path)
    except:
        raise NameError(f"{file_path} does not exists")
    f = ROOT.TFile.Open(file_path)
    try:
        h = f.Get(f"{prefix}/QCDEnriched/{id}/{syst}/ptCorr"); h.SetDirectory(0)
        f.Close()
        return h
    except:
        print(f"Wrong histogram path {prefix}/QCDEnriched/{id}/{syst}/ptCorr for sample {sample}")
        f.Close()
        return None
    

def make_data(sample, id):
    data = {}
    
    for syst in SYSTs:
        rateList = []
        for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
            if syst == "Central":
                h = get_hist(sample, ptCorr, abseta, id)
                err = c_double()
                rate = h.IntegralAndError(h.FindBin(1.), h.FindBin(101.), err)
                rateList.append(rate)
            elif syst == "Stat":
                h = get_hist(sample, ptCorr, abseta, id)
                err = c_double()
                rate = h.IntegralAndError(h.FindBin(1.), h.FindBin(101.), err)
                rateList.append(err.value)
            else:
                if sample == DataStream:
                    if syst in ["MotherJetPtUp", "MotherJetPtDown", "RequireHeavyTag"]:
                        h = get_hist(sample, ptCorr, abseta, id, syst)
                        rateList.append(h.Integral())
                    else:
                        rateList.append(0.)
                else:
                    h = get_hist(sample, ptCorr, abseta, id, syst)
                    if h is None:
                        rateList.append(-999.)
                    else:
                        rateList.append(h.Integral())
        data[syst] = rateList 
    return data

index_col = []
for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
    prefix = findbin(ptCorr, abseta)
    index_col.append(prefix)

data = make_data(DataStream, "loose")
df = pd.DataFrame(data=data, index=index_col)
csv_path = f"results/{args.era}/CSV/{args.measure}/{DataStream}_loose.csv"
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
df.to_csv(csv_path)

data = make_data(DataStream, "tight")
df = pd.DataFrame(data=data, index=index_col)
csv_path = f"results/{args.era}/CSV/{args.measure}/{DataStream}_tight.csv"
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
df.to_csv(csv_path)

for sample, id in product(MCList, ["loose", "tight"]):
    #print(sample, id)
    data = make_data(sample, id)
    df = pd.DataFrame(data=data, index=index_col)
    csv_path = f"results/{args.era}/CSV/{args.measure}/{sample}_{id}.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path) 
