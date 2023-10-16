import os
import argparse
import pandas as pd
import ROOT
from itertools import product
from array import array
from ctypes import c_double
from math import pow, sqrt

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--measure", required=True, type=str, help="electron / muon")
args = parser.parse_args()

#### Settings
WORKDIR = os.environ["WORKDIR"]
ptCorr_bins = []
abseta_bins = []
#QCD = ["QCD"]
if args.measure == "electron":
    ptCorr_bins = [10., 15., 20., 25., 35., 50., 100.]
    abseta_bins = [0., 0.8, 1.479, 2.5]
    #QCD = ["QCD_EMEnriched", "QCD_bcToE"]
    #QCD = ["QCD_EMEnriched"]
    QCD = ["QCD_bcToE"]
elif args.measure == "muon":
    DataStream = "DoubleMuon"
    ptCorr_bins = [10., 15., 20., 30., 50., 100.]
    abseta_bins = [0., 0.9, 1.6, 2.4]
    QCD = ["QCD_MuEnriched"]
else:
    raise KeyError(f"Wrong measure {args.measure}")

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

#### Measure fake rates
#### For QCD, no prompt subtraction
index_col = []
for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
    prefix = findbin(ptCorr, abseta)
    index_col.append(prefix)
    
data = {}
fakeList = []
errList = []
for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
    prefix = findbin(ptCorr, abseta)
    if args.measure == "electron":
        if ptCorr < 20.:   hltpath = "MeasFakeEl8"
        elif ptCorr < 35.: hltpath = "MeasFakeEl12"
        else:              hltpath = "MeasFkaeEl23"  
    if args.measure == "muon":
        if ptCorr < 30.: hltpath = "MeasFakeMu8"
        else:            hltpath = "MeasFakeMu17"
    
    rate_qcd_loose = 0.
    rate_qcd_tight = 0.
    err_qcd_loose = 0.
    err_qcd_tight = 0.
    for sample in QCD:
        df_loose = pd.read_csv(f"results/{args.era}/CSV/{args.measure}/{sample}_loose.csv", index_col=0)
        df_tight = pd.read_csv(f"results/{args.era}/CSV/{args.measure}/{sample}_tight.csv", index_col=0) 
        rate_qcd_loose += df_loose.loc[prefix, "Central"]
        rate_qcd_tight += df_tight.loc[prefix, "Central"]
        err_qcd_loose += pow(df_loose.loc[prefix, "Stat"], 2)
        err_qcd_tight += pow(df_tight.loc[prefix, "Stat"], 2)
    err_qcd_loose = sqrt(err_qcd_loose)
    err_qcd_tight = sqrt(err_qcd_tight)
    
    fakerate = rate_qcd_tight / rate_qcd_loose
    error = 0.
    error += pow(err_qcd_tight/rate_qcd_loose, 2)
    error += pow(rate_qcd_tight/pow(rate_qcd_loose, 2)*err_qcd_loose, 2)
    error = sqrt(error)
    fakeList.append(fakerate)
    errList.append(error)
data["Central"] = fakeList
data["Stat"] = errList

df = pd.DataFrame(data=data, index=index_col)
csv_path = f"results/{args.era}/CSV/{args.measure}/fakerate_qcd.csv"
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
df.to_csv(csv_path)

#### Now save the results to root file
rtfile_path = f"results/{args.era}/ROOT/{args.measure}/fakerate_qcd.root"
os.makedirs(os.path.dirname(rtfile_path), exist_ok=True)
f = ROOT.TFile(rtfile_path, "recreate")
h = ROOT.TH2D(f"fakerate", "", len(abseta_bins)-1, array('d', abseta_bins), len(ptCorr_bins)-1, array('d', ptCorr_bins))
h.SetDirectory(0)

df = pd.read_csv(csv_path, index_col=0)
for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
    prefix = findbin(ptCorr, abseta)
    value = df.loc[prefix, "Central"]
    error = df.loc[prefix, "Stat"]
    thisbin = h.FindBin(abseta+1e-5, ptCorr+1e-5)
    h.SetBinContent(thisbin, value)
    h.SetBinError(thisbin, error)

f.cd()
h.Write()
f.Close()
