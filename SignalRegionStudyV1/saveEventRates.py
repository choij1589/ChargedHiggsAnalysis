import os
import ROOT
import pandas as pd
from math import sqrt

from helper.fitResults import getFitSigmaValue
ROOT.gROOT.SetBatch(True)


ERA = "2017"
CHANNEL = "Skim3Mu"

SIGNALs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65", 
           "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
           "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
           "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
BACKGROUNDs = ["nonprompt", "conversion", "diboson", "ttX", "others"]

matrixSysts = ["NonpromptUp", "NonpromptDown"]
convSysts = ["ConversionUp", "ConversionDown"]

if CHANNEL == "Skim1E2Mu":
    promptSysts = ["L1PrefireUp", "L1PrefireDown",
                   "PileupReweightUp", "PileupReweightDown",
                   "MuonIDSFUp", "MuonIDSFDown",
                   "ElectronIDSFUp", "ElectronIDSFDown",
                   "EMuTrigSFUp", "EMuTrigSFDown",
                   "JetResUp", "JetResDown",
                   "JetEnUp", "JetEnDown",
                   "ElectronResUp", "ElectronResDown",
                   "ElectronEnUp", "ElectronEnDown",
                   "MuonEnUp", "MuonEnDown"]
if CHANNEL == "Skim3Mu":
    promptSysts = ["L1PrefireUp", "L1PrefireDown",
                   "PileupReweightUp", "PileupReweightDown",
                   "MuonIDSFUp", "MuonIDSFDown",
                   "DblMuTrigSFUp", "DblMuTrigSFDown",
                   "JetResUp", "JetResDown",
                   "JetEnUp", "JetEnDown",
                   "MuonEnUp", "MuonEnDown"]
systematics = ["Central"] + promptSysts + matrixSysts + convSysts

def getSumEntries(signal, processName, syst="Central"):
    mA = float(signal.split("_")[1].split("-")[1])
    width = getFitSigmaValue(ERA, CHANNEL, mA)
    f = ROOT.TFile.Open(f"samples/{ERA}/{CHANNEL}__/{signal}/{processName}.root")
    tree = f.Get(f"{processName}_{syst}")

    sumW = 0.;
    sumW2 = 0.;
    ## for 1E2Mu channel, mass2 initialized as -999.
    for evt in tree:
        if abs(evt.mass1-mA) < 3*width and abs(evt.mass2-mA) < 3*width:
            sumW += evt.weight*2
            sumW2 += pow(evt.weight*2, 2)
        elif abs(evt.mass1-mA) < 3*width or abs(evt.mass2-mA) < 3*width:
            sumW += evt.weight
            sumW2 += pow(evt.weight, 2)
        else:
            continue
    f.Close()
    value = sumW
    error = sqrt(sumW2)
    return (value, error)

for SIGNAL in SIGNALs:
    print(f"processing {SIGNAL}...")
    os.makedirs(f"results/{ERA}/{CHANNEL}__CutNCount__/{SIGNAL}", exist_ok=True)
    mA = float(SIGNAL.split("_")[1].split("-")[1])
    preDataFrame = {}

    preDataFrame["signal"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["signal"].append(getSumEntries(SIGNAL, SIGNAL))
        elif syst in promptSysts: preDataFrame["signal"].append(getSumEntries(SIGNAL, SIGNAL, syst))
        else:                     preDataFrame["signal"].append("-")

    preDataFrame["nonprompt"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["nonprompt"].append(getSumEntries(SIGNAL, "nonprompt"))
        elif syst in matrixSysts: preDataFrame["nonprompt"].append(getSumEntries(SIGNAL, "nonprompt", syst))
        else:                     preDataFrame["nonprompt"].append("-")

    preDataFrame["conversion"] = []
    for syst in systematics:
        if syst == "Central":   preDataFrame["conversion"].append(getSumEntries(SIGNAL, "conversion"))
        elif syst in convSysts: preDataFrame["conversion"].append(getSumEntries(SIGNAL, "conversion", syst))
        else:                   preDataFrame["conversion"].append("-")

    preDataFrame["diboson"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["diboson"].append(getSumEntries(SIGNAL, "diboson"))
        elif syst in promptSysts: preDataFrame["diboson"].append(getSumEntries(SIGNAL, "diboson", syst))
        else:                     preDataFrame["diboson"].append("-")

    preDataFrame["ttX"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["ttX"].append(getSumEntries(SIGNAL, "ttX"))
        elif syst in promptSysts: preDataFrame["ttX"].append(getSumEntries(SIGNAL, "ttX", syst))
        else:                     preDataFrame["ttX"].append("-")

    preDataFrame["others"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["others"].append(getSumEntries(SIGNAL, "others"))
        elif syst in promptSysts: preDataFrame["others"].append(getSumEntries(SIGNAL, "others", syst))
        else:                     preDataFrame["others"].append("-")

    df = pd.DataFrame(preDataFrame, index=systematics)
    df.to_csv(f"results/{ERA}/{CHANNEL}__CutNCount__/{SIGNAL}/eventRates.csv", index_label="syst")
