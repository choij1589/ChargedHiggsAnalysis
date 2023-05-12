import os
import ROOT as R
import pandas as pd
R.gROOT.SetBatch(True)

ERA = "2018"
CHANNEL = "Skim3Mu"
NETWORK = ""


SIGNALs = ["MHc-70_MA-15", "MHc-100_MA-15", "MHc-130_MA-15", "MHc-160_MA-15",
           "MHc-70_MA-40", "MHc-130_MA-55", "MHc-100_MA-60", "MHc-70_MA-65",
           "MHc-160_MA-85", "MHc-130_MA-90", "MHc-100_MA-95", "MHc-160_MA-120",
           "MHc-130_MA-125", "MHc-160_MA-155"]
#SIGNALs = ["MHc-70_MA-65", "MHc-160_MA-85", "MHc-130_MA-90", "MHc-100_MA-95", "MHc-160_MA-120"]
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
    with open(f"samples/{ERA}/{CHANNEL}__/interpolResults.csv") as f:
        line = f.readlines()[2].split(",")
    a0 = float(line[0])
    a1 = float(line[1])
    a2 = float(line[2])
    return a0 + a1*mA + a2*(mA**2)

def getHist(processName, signal, syst="Central"):
    mA = float(signal.split("_")[1].split("-")[1])
    sigma = getFitSigmaValue(mA)
    if syst == "Central":
        h = R.TH2D(f"{processName}", "", 20, mA-5*sigma, mA+5*sigma, 20, mA-5*sigma, mA+5*sigma)
    else:
        h = R.TH2D(f"{processName}_{syst}", "", 20, mA-5*sigma, mA+5*sigma, 20, mA-5*sigma, mA+5*sigma)
    
    if ("Net" in NETWORK):  f = R.TFile.Open(f"samples/{ERA}/{CHANNEL}__{NETWORK}__/{signal}/{processName}.root")
    else:                   f = R.TFile.Open(f"samples/{ERA}/{CHANNEL}__/{signal}/{processName}.root")
    tree = f.Get(f"{processName}_{syst}")

    for evt in tree:
        h.Fill(evt.mass1, evt.mass2, evt.weight)
    h.SetDirectory(0)
    
    return h

for SIGNAL in SIGNALs:
    print(f"@@@@ processing {SIGNAL}...")
    if ("Net" in NETWORK):  basePath = f"results/{ERA}/{CHANNEL}__{NETWORK}__/{SIGNAL}"
    else:                   basePath = f"results/{ERA}/{CHANNEL}__/{SIGNAL}"
    os.makedirs(basePath, exist_ok=True)

    mA = float(SIGNAL.split("_")[1].split("-")[1])
    sigma = getFitSigmaValue(mA)
    f = R.TFile(f"{basePath}/shapes_input.root", "recreate")
    data = R.TH2D("data_obs", "", 20, mA-5*sigma, mA+5*sigma, 20, mA-5*sigma, mA+5*sigma)
    for syst in systematics:
        if syst == "Central":     h = getHist(SIGNAL, SIGNAL)
        elif syst in promptSysts: h = getHist(SIGNAL, SIGNAL, syst)
        else:                     continue
        f.cd()
        h.Write()
    
    for syst in systematics:
        if syst == "Central":     
            h = getHist("nonprompt", SIGNAL)
            data.Add(h)
        elif syst in matrixSysts: 
            h = getHist("nonprompt", SIGNAL, syst)
        else:                     
            continue
        f.cd()
        h.Write()

    for syst in systematics:
        if syst == "Central":   
            h = getHist("conversion", SIGNAL)
            data.Add(h)
        elif syst in convSysts: 
            h = getHist("conversion", SIGNAL, syst)
        else:                   
            continue
        f.cd()
        h.Write()

    for syst in systematics:
        if syst == "Central":     
            h = getHist("diboson", SIGNAL)
            data.Add(h)
        elif syst in promptSysts: 
            h = getHist("diboson", SIGNAL, syst)
        else:                     
            continue
        f.cd()
        h.Write()

    for syst in systematics:
        if syst == "Central":     
            h = getHist("ttX", SIGNAL)
            data.Add(h)
        elif syst in promptSysts: 
            h = getHist("ttX", SIGNAL, syst)
        else:                     
            continue
        f.cd()
        h.Write()
    
    for syst in systematics:
        if syst == "Central":     
            h = getHist("others", SIGNAL)
            data.Add(h)
        elif syst in promptSysts: 
            h = getHist("others", SIGNAL, syst)
        else:                     
            continue
        f.cd()
        h.Write()
    data.Write()
    f.Close()
