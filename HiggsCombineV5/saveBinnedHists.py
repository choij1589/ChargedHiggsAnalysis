import os
import ROOT
import numpy as np
import pandas as pd
import joblib

from helper.fitResults import getFitSigmaValue
from helper.MLResults import parseMLCut
ROOT.gROOT.SetBatch(True)

ERA = "2016preVFP"
CHANNEL = "Skim3Mu"
METHOD = "GNNOptim"    # Shape / GNNOptim
doOptim = True if "Optim" in METHOD else False

SIGNALs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
           "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
           "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
           "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
if doOptim:
    SIGNALs = ["MHc-70_MA-65",
               "MHc-100_MA-95",
               "MHc-130_MA-90",
               "MHc-160_MA-85",
               "MHc-160_MA-120"]

BACKGROUNDs = ["nonprompt", "conversion", "diboson", "ttX", "others"]

matrixSysts = ["NonpromptUp", "NonpromptDown"]
convSysts = ["ConversionUp", "ConversionDown"]
promptSysts = ["L1PrefireUp", "L1PrefireDown",
               "PileupReweightUp", "PileupReweightDown",
               "MuonIDSFUp", "MuonIDSFDown",
               "DblMuTrigSFUp", "DblMuTrigSFDown",
               "JetResUp", "JetResDown",
               "JetEnUp", "JetEnDown",
               "MuonEnUp", "MuonEnDown"]
systematics = ["Central"] + promptSysts + matrixSysts + convSysts

def getHist(processName, signal, syst="Central"):
    mA = float(signal.split("_")[1].split("-")[1])
    sigma = getFitSigmaValue(ERA, CHANNEL, mA)
    if syst == "Central":
        h = ROOT.TH1D(f"{processName}", "", 15, mA-5*sigma, mA+5*sigma)
    else:
        h = ROOT.TH1D(f"{processName}_{syst}", "", 15, mA-5*sigma, mA+5*sigma)
    
    f = ROOT.TFile.Open(f"samples/{ERA}/{CHANNEL}__GraphNet__/{signal}/{processName}.root")
    tree = f.Get(f"{processName}_{syst}")
    
    if doOptim:
        # eval score first
        clf = joblib.load(f"results/{ERA}/{CHANNEL}__{METHOD}__/{signal}/classifier.pkl")
        cut = parseMLCut(ERA, CHANNEL, signal)
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
    else:
        for evt in tree:
            h.Fill(evt.mass1, evt.weight)
            h.Fill(evt.mass2, evt.weight)
        h.SetDirectory(0)

    return h

for SIGNAL in SIGNALs:
    print(f"@@@@ processing {SIGNAL}...")
    basePath = f"results/{ERA}/{CHANNEL}__{METHOD}__/{SIGNAL}"
    os.makedirs(basePath, exist_ok=True)

    mA = float(SIGNAL.split("_")[1].split("-")[1])
    sigma = getFitSigmaValue(ERA, CHANNEL, mA)
    f = ROOT.TFile(f"{basePath}/shapes_input.root", "recreate")
    data_obs = ROOT.TH1D("data_obs", "", 15, mA-5*sigma, mA+5*sigma)
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
