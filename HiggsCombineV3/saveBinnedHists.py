import os
import ROOT as R
import numpy as np
import pandas as pd
import joblib
R.gROOT.SetBatch(True)

ERA = "2016postVFP"
CHANNEL = "Skim3Mu"
NETWORK = "GraphNet"


SIGNALs = ["MHc-70_MA-65", "MHc-160_MA-85", "MHc-130_MA-90", "MHc-100_MA-95", "MHc-160_MA-120"]
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

#if ERA == "2016preVFP":
#    scoreDict = {"MHc-70_MA-65": (0.49, 0.05, 0.22),
#                 "MHc-160_MA-85": (0.15, 0.57, 0.45),
#                 "MHc-130_MA-90": (0.63, 0.41, 0.52),
#                 "MHc-100_MA-95": (0.69, 0.47, 0.93),
#                 "MHc-160_MA-120": (0.4, 0.52, 0.78)}
#elif ERA == "2016postVFP":
#    scoreDict = {"MHc-70_MA-65": (0.5, 0.45, 0.57),
#                 "MHc-160_MA-85": (0.59, 0.67, 0.67),
#                 "MHc-130_MA-90": (0.63, 0.6, 0.56),
#                 "MHc-100_MA-95": (0.93, 0.65, 0.63),
#                 "MHc-160_MA-120": (0.49, 0.37, 0.5)}
#elif ERA == "2017":
#    scoreDict = {"MHc-70_MA-65": (0.56, 0.16, 0.48),
#                 "MHc-160_MA-85": (0.43, 0.97, 0.47),
#                 "MHc-130_MA-90": (0.78, 0.94, 0.54),
#                 "MHc-100_MA-95": (0.66, 0.48, 0.57),
#                 "MHc-160_MA-120": (0.44, 0.02, 0.45)}
#elif ERA == "2018":
#    scoreDict = {"MHc-70_MA-65": (0.43, 0.97, 0.4),
#                 "MHc-160_MA-85": (0.21, 0.93, 0.5),
#                 "MHc-130_MA-90": (0.6, 0.4, 0.57),
#                 "MHc-100_MA-95": (0.7, 0.44, 0.91),
#                 "MHc-160_MA-120": (0.4, 0.25, 0.35)}
#else:
#    print(f"Wrong era {ERA}")
#    exit(1)
if ERA == "2016preVFP":
    scoreDict = {"MHc-70_MA-65": 0.54,
                 "MHc-100_MA-95": 0.78, 
                 "MHc-130_MA-90": 0.58,
                 "MHc-160_MA-85": 0.63,
                 "MHc-160_MA-120": 0.75}
elif ERA == "2016postVFP":
    scoreDict = {"MHc-70_MA-65": 0.43,
                 "MHc-100_MA-95": 0.62,
                 "MHc-130_MA-90": 0.72,
                 "MHc-160_MA-85": 0.54,
                 "MHc-160_MA-120": 0.7}
elif ERA == "2017":
    scoreDict = {"MHc-70_MA-65": 0.7,
                 "MHc-100_MA-95": 0.68,
                 "MHc-130_MA-90": 0.6,
                 "MHc-160_MA-85": 0.66,
                 "MHc-160_MA-120": 0.68}
elif ERA == "2018":
    scoreDict = {"MHc-70_MA-65": 0.6,
                 "MHc-100_MA-95": 0.68,
                 "MHc-130_MA-90": 0.66,
                 "MHc-160_MA-85": 0.63,
                 "MHc-160_MA-120": 0.62}
else:
    print(f"Wrong era {ERA}")
    exit(1)

backgrounds = ["nonprompt", "conversion", "ttX", "diboson", "others"]


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
    cut = scoreDict[signal]
    clf = joblib.load(f"results/{ERA}/{CHANNEL}__{NETWORK}__/{signal}/classifier.pkl")
    if syst == "Central":
        h = R.TH1D(f"{processName}", "", 20, mA-5*sigma, mA+5*sigma)
    else:
        h = R.TH1D(f"{processName}_{syst}", "", 20, mA-5*sigma, mA+5*sigma)
    
    if ("Net" in NETWORK):  f = R.TFile.Open(f"samples/{ERA}/{CHANNEL}__{NETWORK}__/{signal}/{processName}.root")
    else:                   f = R.TFile.Open(f"samples/{ERA}/{CHANNEL}__/{signal}/{processName}.root")
    tree = f.Get(f"{processName}_{syst}")
    
    # eval score first
    inputs = []
    weights = []
    masses = []
    for evt in tree:
        inputs.append([evt.scoreX, evt.scoreY, evt.scoreZ])
        weights.append(evt.weight)
        masses.append((evt.mass1, evt.mass2))
    scores = clf.predict_proba(inputs)
    for score, weight, mass in zip(scores, weights, masses):
        if score[1] > cut:
            h.Fill(mass[0], weight)
            h.Fill(mass[1], weight)
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
    data_obs = R.TH1D("data_obs", "", 20, mA-5*sigma, mA+5*sigma)
    print(f"@@@@ processing signal...")
    for syst in systematics:
        if syst == "Central":     h = getHist(SIGNAL, SIGNAL)
        elif syst in promptSysts: h = getHist(SIGNAL, SIGNAL, syst)
        else:                     continue
        f.cd(); h.Write()
    
    print(f"@@@@ processing nonprompt...")
    for syst in systematics:
        if syst == "Central":     
            h = getHist("nonprompt", SIGNAL)
            data_obs.Add(h)
        elif syst in matrixSysts: 
            h = getHist("nonprompt", SIGNAL, syst)
        else:                     
            continue
        f.cd(); h.Write()

    print(f"@@@@ processing conversion...")
    for syst in systematics:
        if syst == "Central":   
            h = getHist("conversion", SIGNAL)
            data_obs.Add(h)
        elif syst in convSysts: 
            h = getHist("conversion", SIGNAL, syst)
        else:                   
            continue
        f.cd(); h.Write()

    print(f"@@@@ processing diboson...")
    for syst in systematics:
        if syst == "Central":     
            h = getHist("diboson", SIGNAL)
            data_obs.Add(h)
        elif syst in promptSysts: 
            h = getHist("diboson", SIGNAL, syst)
        else:                     
            continue
        f.cd(); h.Write()

    print(f"@@@@ processing ttX...")
    for syst in systematics:
        if syst == "Central":     
            h = getHist("ttX", SIGNAL)
            data_obs.Add(h)
        elif syst in promptSysts: 
            h = getHist("ttX", SIGNAL, syst)
        else:                     
            continue
        f.cd(); h.Write()
    
    print(f"@@@@ processing others...")
    for syst in systematics:
        if syst == "Central":     
            h = getHist("others", SIGNAL)
            data_obs.Add(h)
        elif syst in promptSysts: 
            h = getHist("others", SIGNAL, syst)
        else:                     
            continue
        f.cd(); h.Write()

    # make data
    f.cd()
    data_obs.Write()
    f.Close()
