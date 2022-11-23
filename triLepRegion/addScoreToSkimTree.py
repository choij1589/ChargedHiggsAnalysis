import os, sys; sys.path.insert(0, os.environ["WORKDIR"])
import argparse
import pandas as pd

import torch
from array import array
from itertools import product
from math import sin
from ROOT import TFile, TTree

from libPython.MLTools import ParticleNet, ParticleNetLite
from libPython.DataFormat import Particle, Muon, Electron, Jet
from libPython.Preprocessor import evt_to_graph
from libPython.Management import predict_proba

parser = argparse.ArgumentParser()
parser.add_argument("--sample", "-s", required=True, type=str, help="sample name")
parser.add_argument("--era", "-e", required=True, type=str, help="era")
args = parser.parse_args()


# load models
csv = pd.read_csv("MetaInfo/modelInfo.csv", sep=",\s", engine="python", comment="#")
modelDict = dict()

def loadModel(model, modelPath):
    if model == "ParticleNet":
        out = ParticleNet(num_features=9, num_classes=2)
    elif model == "ParticleNetLite":
        out = ParticleNetLite(num_features=9, num_classes=2)
    else:
        print(f"wrong model name {model}")
        raise(NameError)
    out.load_state_dict(torch.load(modelPath, map_location=torch.device("cpu")))
    return out

for idx in csv.index:
    channel = csv.loc[idx, 'channel']
    sig, bkg = csv.loc[idx, 'signal'], csv.loc[idx, 'background']
    model = csv.loc[idx, 'model']
    optim = csv.loc[idx, 'optimizer']
    initLR = float(csv.loc[idx, 'initLR'])
    scheduler = csv.loc[idx, 'scheduler']
    
    modelPath = f"{os.environ['WORKDIR']}/triLepRegion/pilot/{channel}__/{sig}_vs_{bkg}/models/{model}_{optim}_initLR-{str(initLR).replace('.','p')}_{scheduler}.pt"
    modelDict[f"score_{channel}_{sig}_vs_{bkg}"] = loadModel(model, modelPath)

# TFiles
f = TFile.Open(f"{args.sample}", "read")
outpath = f"{args.sample}".replace("SS2lOR3l", "HcToWA")
if not os.path.exists(os.path.dirname(outpath)):
    os.makedirs(os.path.dirname(outpath))
fout = TFile.Open(outpath, "recreate")

oldtree = f.Get("recoTree/SKFlat")
newtree = oldtree.CloneTree(0)

# set branches
scoreDict = dict()
for name in modelDict.keys():
    scoreDict[name] = array("f", [0])
    newtree.Branch(name, scoreDict[name], f"{name}/F")

for evt in oldtree:
    muons = []
    muons_zip = zip(evt.muon_pt, evt.muon_eta, evt.muon_phi, evt.muon_mass, evt.muon_charge)
    for pt, eta, phi, mass, charge in muons_zip:
        # print(pt, eta, phi, mass, charge)
        this_muon = Muon(pt, eta, phi, mass)
        this_muon.SetCharge(charge)
        muons.append(this_muon)

    electrons = []
    electrons_zip = zip(evt.electron_eta, evt.electron_phi, evt.electron_Energy, evt.electron_charge)
    for eta, phi, energy, charge in electrons_zip:
        el = Electron(0., 0., 0., 0.)
        el.SetPtEtaPhiE(1., eta, phi, energy)
        theta = el.Theta()
        pt = energy * sin(theta)
        el.SetPtEtaPhiE(pt, eta, phi, energy)
        el.SetCharge(charge)
        electrons.append(el)

    jets = []
    jets_zip = zip(evt.jet_pt, evt.jet_eta, evt.jet_phi, evt.jet_m, evt.jet_charge, evt.jet_DeepFlavour)
    for pt, eta, phi, mass, charge, bscore in jets_zip:
        this_jet = Jet(pt, eta, phi, mass)
        this_jet.SetCharge(charge)
        this_jet.SetBtagScore(bscore)
        jets.append(this_jet)

    METv = Particle(evt.pfMET_pt, 0., evt.pfMET_phi, 0.)
    objects = muons + electrons + jets; objects.append(METv)
    node_list = []
    for particle in objects:
        node_list.append([particle.E(), particle.Px(), particle.Py(), particle.Pz(),
                          particle.Charge(), particle.IsMuon(), particle.IsElectron(),
                          particle.IsJet(), particle.BtagScore()])
    data = evt_to_graph(node_list, y=None, k=4) 
    for name, classifier in modelDict.items():
       scoreDict[name] = array("f", [predict_proba(classifier, data.x, data.edge_index)])
    newtree.Fill()

fout.mkdir("recoTree")
fout.cd("recoTree")
newtree.Write()

f.Close()
fout.Close()
