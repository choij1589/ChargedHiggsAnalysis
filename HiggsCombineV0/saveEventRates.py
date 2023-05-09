import ROOT as R
import pandas as pd
R.gROOT.SetBatch(True)


ERA = "2017"
CHANNEL = "Skim3Mu"
NETWORK = "DenseNet"

SIGNALs = ["MHc-70_MA-15", "MHc-100_MA-15", "MHc-130_MA-15", "MHc-160_MA-15",
           "MHc-70_MA-40", "MHc-130_MA-55", "MHc-100_MA-60", "MHc-70_MA-65",
           "MHc-160_MA-85", "MHc-130_MA-90", "MHc-100_MA-95", "MHc-160_MA-120",
           "MHc-130_MA-125", "MHc-160_MA-155"]
BACKGROUNDs = ["nonprompt", "conversion", "diboson", "ttX", "others"]

matrixSysts = ["NonpromptUp", "NonpromptDown"]
convSysts = ["ConversionUp", "ConversionDown"]
promptSysts = ["L1PrefireUp", "L1PrefireDown",
               "PileupReweightUp", "PileupReweightDown",
               "MuonIDSFUp", "MuonIDSFDown",
               "DblMuTrigSFUp", "DblMuTrigSFDown",
               "JetResUp", "JetResDown",
               "JetEnUp", "JetEnDown",
               "MuonEnUp", "MuonEnDown",
               "ElectronEnUp", "ElectronEnDown",
               "ElectronResUp", "ElectronResDown"]
systematics = ["Central"] + promptSysts + matrixSysts + convSysts

def getFitSigmaValue(mA):
    with open(f"results/{ERA}/{CHANNEL}__/interpolResults.csv") as f:
        line = f.readlines()[2].split(",")
    a0 = float(line[0])
    a1 = float(line[1])
    a2 = float(line[2])
    
    return a0 + a1*mA + a2*(mA**2)

def getSumEntries(processName, syst="Central"):
    width = getFitSigmaValue(MA)
    f = R.TFile.Open(f"samples/{ERA}/{CHANNEL}__{NETWORK}__/{processName}.root")
    tree = f.Get(f"{processName}_{syst}")

    mass = R.RooRealVar("mass", "mass", MA, MA-5*width, MA+5*width)
    weight = R.RooRealVar("weight", "weight", -10., 10.)

    mc = R.RooDataSet("mc", "mc", tree, R.RooArgSet(mass, weight), "", "weight")
    return mc.sumEntries()


for SIGNAL in SIGNALs:
    MA = float(SIGNAL.split("_")[1].split("-")[1])
    preDataFrame = {}

    preDataFrame["signal"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["signal"].append(getSumEntries(SIGNAL))
        elif syst in promptSysts: preDataFrame["signal"].append(getSumEntries(SIGNAL, syst))
        else:                     preDataFrame["signal"].append("-")

    preDataFrame["nonprompt"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["nonprompt"].append(getSumEntries("nonprompt"))
        elif syst in matrixSysts: preDataFrame["nonprompt"].append(getSumEntries("nonprompt", syst))
        else:                     preDataFrame["nonprompt"].append("-")

    preDataFrame["conversion"] = []
    for syst in systematics:
        if syst == "Central":   preDataFrame["conversion"].append(getSumEntries("conversion"))
        elif syst in convSysts: preDataFrame["conversion"].append(getSumEntries("conversion", syst))
        else:                   preDataFrame["conversion"].append("-")

    preDataFrame["diboson"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["diboson"].append(getSumEntries("diboson"))
        elif syst in promptSysts: preDataFrame["diboson"].append(getSumEntries("diboson", syst))
        else:                     preDataFrame["diboson"].append("-")

    preDataFrame["ttX"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["ttX"].append(getSumEntries("ttX"))
        elif syst in promptSysts: preDataFrame["ttX"].append(getSumEntries("ttX", syst))
        else:                     preDataFrame["ttX"].append("-")

    preDataFrame["others"] = []
    for syst in systematics:
        if syst == "Central":     preDataFrame["others"].append(getSumEntries("others"))
        elif syst in promptSysts: preDataFrame["others"].append(getSumEntries("others", syst))
        else:                     preDataFrame["others"].append("-")

    df = pd.DataFrame(preDataFrame, index=systematics)
    df.to_csv(f"results/{ERA}/{CHANNEL}__/{SIGNAL}.csv", index_label="syst")
