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
DataStream = ""
ptCorr_bins = []
abseta_bins = []
SYSTs = []

if args.measure == "electron":
    if "2016" in args.era:  DataStream = "DoubleEG"
    if "2017" in args.era:  DataStream = "SingleElectron"
    if "2018" in args.era:  DataStream = "EGamma"
    ptCorr_bins = [10., 15., 20., 25., 35., 50., 100.]
    abseta_bins = [0., 0.8, 1.579, 2.5]
    PromptVariation = [["Stat"],
                       ["PileupReweight"],
                       ["L1PrefireUp", "L1PrefireDown"],
                       ["ElectronRecoSFUp", "ElectronRecoSFDown"],
                       ["JetResUp", "JetResDown"],
                       ["JetEnUp", "JetEnDown"],
                       ["ElectronResUp", "ElectronResDown"],
                       ["ElectronEnUp", "ElectronEnDown"],
                       ["MuonEnUp", "MuonEnDown"]]
    HLTPATHs = ["MeasFakeEl8", "MeasFakeEl12", "MeasFakeEl23"]
elif args.measure == "muon":
    DataStream = "DoubleMuon"
    ptCorr_bins = [10., 15., 20., 30., 50., 100.]
    abseta_bins = [0., 0.9, 1.6, 2.4]
    PromptVaration = [['Stat'],
                      ["PileupReweight"],
                      ["L1PrefireUp", "L1PrefireDown"],
                      ["MuonRecoSFUp", "MuonRecoSFDown"],
                      ["JetResUp", "JetResDown"],
                      ["JetEnUp", "JetEnDown"],
                      ["ElectronResUp", "ElectronResDown"],
                      ["ElectronEnUp", "ElectronEnDown"],
                      ["MuonEnUp", "MuonEnDown"]]
    HLTPATHs = ["MeasFakeMu8", "MeasFakeMu17"]
else:
    raise KeyError(f"Wrong measure {args.measure}")
SelectionVartion = [["PromptNormUp", "PromptNormDown"],
                    ["MotherJetPtUp", "MotherJetPtDown"],
                    ["RequireHeavyTag"]]
IDs = ["loose", "tight"]

W  = ["WJets_MG"]
DY = ["DYJets", "DYJets10to50_MG"]
TT = ["TTLL_powheg"]
VV = ["WW_pythia", "WZ_pythia", "ZZ_pythia"]
ST = ["SingleTop_sch_Lep", "SingleTop_tch_top_Incl", "SingleTop_tch_antitop_Incl",
      "SingleTop_tW_top_NoFullyHad", "SingleTop_tW_antitop_NoFullyHad"]
MCList = W + DY + TT + VV + ST

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
            prefix += f"_abseta_{str(abseta_bins[i]).replace('.', 'p')}to{str(abseta_bins[i]).replace('.', 'p')}"
    return prefix

#### First evaluate central scale for product(hltpaths, ids)
def get_prompt_scale(hltpath, id, syst):
    file_path = f"{WORKDIR}/data/MeasFakeRateV4/{args.era}/{hltpath}__/DATA/MeasFakeRateV4_{DataStream}.root"
    assert os.path.exists(file_path)
    f = ROOT.TFile.Open(file_path)
    data = f.Get(f"ZEnriched/{id}/Central/pair/mass"); data.SetDirectory(0)
    f.Close()
    
    stat_data = c_double()
    rate_data = data.IntegralAndError(data.FindBin(50), data.FindBin(150), stat_data)
    stat_data = stat_data.value
    
    rate_mc = 0.
    stat_mc = 0.
    for sample in MCList:
        file_path = f"{WORKDIR}/data/MeasFakeRateV4/{args.era}/{hltpath}__RunSyst__/MeasFakeRateV4_{sample}.root"
        assert os.path.exists(file_path)
        f = ROOT.TFile.Open(file_path)
        try:
            h = f.Get(f"ZEnriched/{id}/{syst}/pair/mass");   h.SetDirectory(0)
            this_stat = c_double()
            rate_mc += h.IntegralAndError(h.FindBin(50), h.FindBin(150), this_stat)
            stat_mc += pow(this_stat.value, 2)
        except:
            print(sample)
            continue
        f.Close()
    stat_mc = sqrt(stat_mc)
    
    scale = rate_data / rate_mc
    scaleUp = (rate_data+stat_data) / (rate_mc-stat_mc)
    scaleDown = (rate_data-stat_data) / (rate_mc+stat_mc)
    return (scale, scaleUp, scaleDown)

#### measure prompt scale in Z-enriched region
def get_final_scale(hltpath, id):
    scale, scaleUp, scaleDown = get_prompt_scale(hltpath, id, "Central")
    stat = max(abs(scaleUp-scale), abs(scaleDown-scale))
    totalUnc = pow(stat, 2)
    for systList in PromptVaration:
        if len(systList) == 1:
            syst = systList[0]
            if syst == "Stat": continue 
            this_scale, _, _ = get_prompt_scale(hltpath, id, syst)
            totalUnc += pow(this_scale-scale, 2)
        else:
            systUp, systDown = tuple(systList)
            this_scaleUp, _, _ = get_prompt_scale(hltpath, id, systUp)
            this_scaleDown, _, _ = get_prompt_scale(hltpath, id, systDown)
            this_error = max(abs(this_scaleUp - scale), abs(this_scaleDown - scale))
            totalUnc += pow(this_error, 2)
    totalUnc = sqrt(totalUnc)
    return (scale, totalUnc, totalUnc/scale)

#### Measure fake rates
#### For prompt normalization, assign 10% variation
scaleDict = {}
for hltpath, id in product(HLTPATHs, IDs):
    scale, _, _ = get_prompt_scale(hltpath, id, syst="Central")
    scaleDict[f"{hltpath}_{id}"] = scale

index_col = []
for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
    prefix = findbin(ptCorr, abseta)
    index_col.append(prefix)

data = {}
for syst in ["Central", "StatUp", "StatDown",  "PromptNormUp", "PromptNormDown", "MotherJetPtUp", "MotherJetPtDown", "RequireHeavyTag"]:
    fakeList = []
    for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
        prefix = findbin(ptCorr, abseta)
    
        if ptCorr < 30.: hltpath = "MeasFakeMu8"
        else:            hltpath = "MeasFakeMu17"
    
        # data
        df_loose = pd.read_csv(f"results/{args.era}/CSV/{args.measure}/{DataStream}_loose.csv", index_col=0)
        df_tight = pd.read_csv(f"results/{args.era}/CSV/{args.measure}/{DataStream}_tight.csv", index_col=0) 
        rate_data_loose = df_loose.loc[prefix, "Central"]
        rate_data_tight = df_tight.loc[prefix, "Central"]
        
        if syst == "StatUp":
            rate_data_loose += df_loose.loc[prefix, "Stat"]
            rate_data_tight += df_tight.loc[prefix, "Stat"]
        if syst == "StatDown":
            rate_data_loose -= df_loose.loc[prefix, "Stat"]
            rate_data_tight -= df_tight.loc[prefix, "Stat"]
    
        # prompt
        rate_prompt_loose = 0.
        rate_prompt_tight = 0.
        for sample in MCList:
            df_loose = pd.read_csv(f"results/{args.era}/CSV/{args.measure}/{sample}_loose.csv", index_col=0)
            df_tight = pd.read_csv(f"results/{args.era}/CSV/{args.measure}/{sample}_tight.csv", index_col=0) 
            if syst in ["Central", "PromptNormUp", "PromptNormDown"]:
                rate_prompt_loose += df_loose.loc[prefix, "Central"]
                rate_prompt_tight += df_tight.loc[prefix, "Central"]
            elif syst == "StatUp":
                rate_prompt_loose += (df_loose.loc[prefix, "Central"]+df_loose.loc[prefix, "Stat"])
                rate_prompt_tight += (df_tight.loc[prefix, "Central"]+df_tight.loc[prefix, "Stat"])
            elif syst == "StatDown":
                rate_prompt_loose += (df_loose.loc[prefix, "Central"]-df_loose.loc[prefix, "Stat"])
                rate_prompt_tight += (df_tight.loc[prefix, "Central"]-df_tight.loc[prefix, "Stat"])
            else:
                rate_prompt_loose += df_loose.loc[prefix, syst]
                rate_prompt_tight += df_tight.loc[prefix, syst]
        scale = 1.
        if syst == "PromptNormUp":   scale = 1.1
        if syst == "PromptNormDown": scale = 0.9
        rate_prompt_loose *= scaleDict[f"{hltpath}_loose"]*scale
        rate_prompt_tight *= scaleDict[f"{hltpath}_tight"]*scale
    
        #print(rate_data_loose, rate_prompt_loose)
        #print(rate_data_tight, rate_prompt_tight)
        fakerate = (rate_data_tight-rate_prompt_tight) / (rate_data_loose-rate_prompt_loose)
        fakeList.append(fakerate)
    data[syst] = fakeList
df = pd.DataFrame(data=data, index=index_col)
csv_path = f"results/{args.era}/CSV/{args.measure}/fakerate.csv"
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
df.to_csv(csv_path)

#### now save the results
rtfile_path = f"results/{args.era}/ROOT/{args.measure}/fakerate.root"
os.makedirs(os.path.dirname(rtfile_path), exist_ok=True)
f = ROOT.TFile(rtfile_path, "recreate")
# make histograms
hists = {}
h = ROOT.TH2D(f"fakerate", "", len(abseta_bins)-1, array('d', abseta_bins), len(ptCorr_bins)-1, array('d', ptCorr_bins))
h.SetDirectory(0)
hists["TotalUnc"] = h
for syst in ["Central", "PromptNormUp", "PromptNormDown", "MotherJetPtUp", "MotherJetPtDown", "RequireHeavyTag"]:
    hists[syst] = h.Clone(f"fakerate_{syst}")

# save contents
df = pd.read_csv(csv_path, index_col=0)
for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
    prefix = findbin(ptCorr, abseta)
    thisbin = hists[syst].FindBin(abseta+1e-5, ptCorr+1e-5)
    for syst in ["Central", "PromptNormUp", "PromptNormDown", "MotherJetPtUp", "MotherJetPtDown", "RequireHeavyTag"]:
        if syst == "Central":
            value = df.loc[prefix, "Central"]
            stat = max(abs(df.loc[prefix, "StatUp"] - df.loc[prefix, "Central"]), abs(df.loc[prefix, "StatDown"]))
        else:
            value = df.loc[prefix, syst]
            stat = 0.
        hists[syst].SetBinContent(thisbin, value)
        hists[syst].SetBinError(thisbin, stat)

# estimate total systematics
for ptCorr, abseta in product(ptCorr_bins[:-1], abseta_bins[:-1]):
    prefix = findbin(ptCorr, abseta)
    thisbin = hists[syst].FindBin(abseta+1e-5, ptCorr+1e-5) 
    
    value = df.loc[prefix, "Central"]
    stat = max(abs(df.loc[prefix, "StatUp"] - df.loc[prefix, "Central"]), abs(df.loc[prefix, "StatDown"] - df.loc[prefix, "Central"]))
    totalUnc = pow(stat, 2)
    for systList in SelectionVartion:
        if len(systList) == 1:
            syst = systList[0]
            totalUnc += pow(df.loc[prefix, syst]-value, 2)
        else:
            systUp, systDown = tuple(systList)
            thisUnc = max(abs(df.loc[prefix, systUp]-value), abs(df.loc[prefix, systDown]-value))
            totalUnc += pow(thisUnc, 2)
    totalUnc = sqrt(totalUnc)
    print(prefix, value, totalUnc)
    hists["TotalUnc"].SetBinContent(thisbin, value)
    hists["TotalUnc"].SetBinError(thisbin, totalUnc)

for hist in hists.values():
    f.cd()
    hist.Write()
f.Close()
     
