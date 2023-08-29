import os, shutil
import numpy as np
import pandas as pd
from itertools import product, combinations
from ROOT import TFile
from DataFormat import Particle
from Preprocess import getMuons, getElectrons, getJets

# global variables 
WORKDIR = os.environ['WORKDIR']
CHANNEL = "Skim3Mu"

# no. of events to copy
SIGNALs = ["MHc-70_MA-65", "MHc-160_MA-85", "MHc-130_MA-90", "MHc-100_MA-95", "MHc-160_MA-120"]
NONPROMPTs = ["TTLL_powheg", "DYJetsToMuMu_MiNNLO"]
#NONPROMPTs = ["TTLL_powheg", "DYJets_MG"]
DIBOSONs = ["WZTo3LNu_mllmin0p1_powheg", "ZZTo4L_powheg"]
TTZ = ["ttZToLLNuNu"]
BACKGROUNDs = NONPROMPTs + DIBOSONs + TTZ


ERAs = ["2016preVFP", "2016postVFP", "2017", "2018"]
#nEvtsToCopy = {"signal": [20000, 20000, 40000, 60000],
#               "TTLL_powheg": [17000, 17000, 35500, 54000],
#               "DYJetsToMuMu_MiNNLO": [3000, 3000, 4500, 6000],
#               "WZTo3LNu_mllmin0p1_powheg": [10000, 10000, 20000, 30000],
#               "ZZTo4L_powheg": [10000, 10000, 20000, 30000],
#               "ttZToLLNuNu": [20000, 20000, 40000, 60000]}
nEvtsToCopy = {"signal": [15000, 15000, 30000, 45000],
               "TTLL_powheg": [13500, 13500, 27000, 40500],
               "DYJetsToMuMu_MiNNLO": [1500, 1500, 3000, 4500],
               "WZTo3LNu_mllmin0p1_powheg": [7500, 7500, 15000, 22500],
               "ZZTo4L_powheg": [7500, 7500, 15000, 22500],
               "ttZToLLNuNu": [15000, 15000, 30000, 45000]}

# input features
features = []
if CHANNEL == "Skim1E2Mu":
    features = ["mu1_energy", "mu1_px", "mu1_py", "mu1_pz", "mu1_charge",
                "mu2_energy", "mu2_px", "mu2_py", "mu2_pz", "mu2_charge",
                "ele_energy", "ele_px", "ele_py", "ele_pz", "ele_charge",
                "j1_energy", "j1_px", "j1_py", "j1_pz", "j1_charge", "j1_btagScore",
                "j2_energy", "j2_px", "j2_py", "j2_pz", "j2_charge", "j2_btagScore",
                'dR_mu1mu2', 'dR_mu1ele', 'dR_mu2ele', 'dR_j1ele', 'dR_j2ele', "dR_j1j2",
                "HT", "LT", "MT", "MET", "Nj", "Nb",
                "avg_dRjets", "avg_btagScore"
                ]
elif CHANNEL == "Skim3Mu":
    features = ["mu1_energy", "mu1_px", "mu1_py", "mu1_pz", "mu1_charge",
                "mu2_energy", "mu2_px", "mu2_py", "mu2_pz", "mu2_charge",
                "mu3_energy", "mu3_px", "mu3_py", "mu3_pz", "mu3_charge",
                "j1_energy", "j1_px", "j1_py", "j1_pz", "j1_charge", "j1_btagScore",
                "j2_energy", "j2_px", "j2_py", "j2_pz", "j2_charge", "j2_btagScore",
                'dR_mu1mu2', 'dR_mu1mu3', 'dR_mu2mu3',
                'dR_j1mu1', 'dR_j1mu2', "dR_j1mu3",
                "dR_j2mu1", "dR_j2mu2", "dR_j2mu3",
                "dR_j1j2",
                "HT", "LT", "MT1", "MT2", "MT3", "MET", "Nj", "Nb",
                "avg_dRjets", "avg_btagScore"
                ]
else:
    raise(KeyError)

# helper functions
def loop(evt, data):
    muons = getMuons(evt)
    electrons = getElectrons(evt)
    jets, bjets = getJets(evt)
    METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)

    dRjets = []
    for idx1, idx2 in combinations(range(len(jets)), 2):
        dRjets.append(jets[idx1].DeltaR(jets[idx2]))
    dRjets = np.mean(dRjets)

    if CHANNEL == "Skim1E2Mu":
        mu1, mu2 = muons[0], muons[1]
        ele = electrons[0]
        j1, j2 = jets[0], jets[1]
        MT = (ele+METv).Mt()

        data['mu1_energy'].append(mu1.E())
        data['mu1_px'].append(mu1.Px())
        data['mu1_py'].append(mu1.Py())
        data['mu1_pz'].append(mu1.Pz())
        data['mu1_charge'].append(mu1.Charge())
        data['mu2_energy'].append(mu2.E())
        data['mu2_px'].append(mu2.Px())
        data['mu2_py'].append(mu2.Py())
        data['mu2_pz'].append(mu2.Pz())
        data['mu2_charge'].append(mu2.Charge())
        data['ele_energy'].append(ele.E())
        data['ele_px'].append(ele.Px())
        data['ele_py'].append(ele.Py())
        data['ele_pz'].append(ele.Pz())
        data['ele_charge'].append(ele.Charge())
        data['j1_energy'].append(j1.E())
        data['j1_px'].append(j1.Px())
        data['j1_py'].append(j1.Py())
        data['j1_pz'].append(j1.Pz())
        data['j1_charge'].append(j1.Charge())
        data['j1_btagScore'].append(j1.BtagScore())
        data['j2_energy'].append(j2.E())
        data['j2_px'].append(j2.Px())
        data['j2_py'].append(j2.Py())
        data['j2_pz'].append(j2.Pz())
        data['j2_charge'].append(j2.Charge())
        data['j2_btagScore'].append(j2.BtagScore())
        data['dR_mu1mu2'].append(mu1.DeltaR(mu2))
        data['dR_mu1ele'].append(mu1.DeltaR(ele))
        data['dR_mu2ele'].append(mu2.DeltaR(ele))
        data['dR_j1ele'].append(j1.DeltaR(ele))
        data['dR_j2ele'].append(j2.DeltaR(ele))
        data['dR_j1j2'].append(j1.DeltaR(j2))
        data['HT'].append(sum([j.Pt() for j in jets]))
        data['LT'].append(sum([l.Pt() for l in electrons+muons]))
        data['MT'].append(MT)
        data['MET'].append(METv.Pt())
        data['Nj'].append(len(jets))
        data['Nb'].append(len(bjets))
        data['avg_dRjets'].append(dRjets)
        data['avg_btagScore'].append(np.mean([j.BtagScore() for j in jets]))
    elif CHANNEL == "Skim3Mu":
        mu1, mu2, mu3 = muons[0], muons[1], muons[2]
        j1, j2 = jets[0], jets[1]
        MT1 = (mu1+METv).Mt()
        MT2 = (mu2+METv).Mt()
        MT3 = (mu3+METv).Mt()

        data['mu1_energy'].append(mu1.E())
        data['mu1_px'].append(mu1.Px())
        data['mu1_py'].append(mu1.Py())
        data['mu1_pz'].append(mu1.Pz())
        data['mu1_charge'].append(mu1.Charge())
        data['mu2_energy'].append(mu2.E())
        data['mu2_px'].append(mu2.Px())
        data['mu2_py'].append(mu2.Py())
        data['mu2_pz'].append(mu2.Pz())
        data['mu2_charge'].append(mu2.Charge())
        data['mu3_energy'].append(mu3.E())
        data['mu3_px'].append(mu3.Px())
        data['mu3_py'].append(mu3.Py())
        data['mu3_pz'].append(mu3.Pz())
        data['mu3_charge'].append(mu3.Charge())
        data['j1_energy'].append(j1.E())
        data['j1_px'].append(j1.Px())
        data['j1_py'].append(j1.Py())
        data['j1_pz'].append(j1.Pz())
        data['j1_charge'].append(j1.Charge())
        data['j1_btagScore'].append(j1.BtagScore())
        data['j2_energy'].append(j2.E())
        data['j2_px'].append(j2.Px())
        data['j2_py'].append(j2.Py())
        data['j2_pz'].append(j2.Pz())
        data['j2_charge'].append(j2.Charge())
        data['j2_btagScore'].append(j2.BtagScore())
        data['dR_mu1mu2'].append(mu1.DeltaR(mu2))
        data['dR_mu1mu3'].append(mu1.DeltaR(mu3))
        data['dR_mu2mu3'].append(mu2.DeltaR(mu3))
        data['dR_j1mu1'].append(j1.DeltaR(mu1))
        data['dR_j1mu2'].append(j1.DeltaR(mu2))
        data['dR_j1mu3'].append(j1.DeltaR(mu3))
        data['dR_j2mu1'].append(j2.DeltaR(mu1))
        data['dR_j2mu2'].append(j2.DeltaR(mu2))
        data['dR_j2mu3'].append(j2.DeltaR(mu3))
        data['dR_j1j2'].append(j1.DeltaR(j2))
        data['HT'].append(sum([j.Pt() for j in jets]))
        data['LT'].append(sum([l.Pt() for l in muons]))
        data['MT1'].append(MT1)
        data['MT2'].append(MT2)
        data['MT3'].append(MT3)
        data['MET'].append(METv.Pt())
        data['Nj'].append(len(jets))
        data['Nb'].append(len(bjets))
        data['avg_dRjets'].append(dRjets)
        data['avg_btagScore'].append(np.mean([j.BtagScore() for j in jets]))
    else:
        print(f"Wrong channel {CHANNEL}")
        raise(ValueError)


# signal
for era, signal in product(ERAs, SIGNALs):
    nEvts = nEvtsToCopy["signal"][ERAs.index(era)]
    # check no. of events
    f = TFile.Open(f"{WORKDIR}/data/DataPreprocess/{era}/{CHANNEL}__/DataPreprocess_TTToHcToWAToMuMu_{signal}.root")
    tree = f.Get("Events")
    try:
        assert nEvts < tree.GetEntries()
    except:
        print(f"[Warning] small no. of events for {era}-{signal}: nEvts({nEvts}) < nEntries({tree.GetEntries()})")
        print(f"[Warning] force nEvts to no. of tree entries")
        nEvts = tree.GetEntries()
    f.Close()

    # copyfile
    os.system(f"{WORKDIR}/libCpp/copyFile {WORKDIR}/data/DataPreprocess/{era}/{CHANNEL}__/DataPreprocess_TTToHcToWAToMuMu_{signal}.root {nEvts}")
    shutil.move(f"{WORKDIR}/data/DataPreprocess/{era}/{CHANNEL}__/DataPreprocess_TTToHcToWAToMuMu_{signal}_copy.root", f"{WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{signal}_{era}.root")

# hadd events
for signal in SIGNALs:
    os.system(f"hadd -f {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{signal}.root {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{signal}_*.root")
    os.system(f"rm {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{signal}_*.root")

# background
for era, bkg in product(ERAs, BACKGROUNDs):
    nEvts = nEvtsToCopy[bkg][ERAs.index(era)]
    # check no. of events
    f = TFile.Open(f"{WORKDIR}/data/DataPreprocess/{era}/{CHANNEL}__/DataPreprocess_{bkg}.root")
    tree = f.Get("Events")
    try:
        assert nEvts < tree.GetEntries()
    except:
        print(f"[Warning] small no. of events for {era}-{bkg}: nEvts({nEvts}) < nEntries({tree.GetEntries()})")
        print(f"[Warning] force nEvts to no. of tree entries")
        nEvts = tree.GetEntries()
    f.Close()

    # copyfile
    os.system(f"{WORKDIR}/libCpp/copyFile {WORKDIR}/data/DataPreprocess/{era}/{CHANNEL}__/DataPreprocess_{bkg}.root {nEvts}")
    shutil.move(f"{WORKDIR}/data/DataPreprocess/{era}/{CHANNEL}__/DataPreprocess_{bkg}_copy.root", f"{WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{bkg}_{era}.root")

# hadd events
for bkg in BACKGROUNDs:
    os.system(f"hadd -f {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{bkg}.root {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{bkg}_*.root")
    os.system(f"rm {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{bkg}_*.root")
# nonprompt
os.system(f"hadd -f {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/nonprompt.root {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/TTLL_powheg.root {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/DYJets*.root")
# diboson
os.system(f"hadd -f {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/diboson.root {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/WZ*.root {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/ZZ*.root")
# ttZ
os.system(f"mv {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/ttZToLLNuNu.root {WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/ttZ.root")

# convert root files to csv format
for sample in SIGNALs + ["nonprompt", "diboson", "ttZ"]:
    print(f"@@@@ converting {sample}.root to {sample}.csv ...")
    f = TFile.Open(f"{WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/{sample}.root")
    data = {}
    for feature in features:
        data[feature] = []
    for ev in f.Events:
        loop(ev, data)
    f.Close()
    df = pd.DataFrame(data, columns=features)
    df.to_csv(f"{WORKDIR}/data/DataPreprocess/Combined/{CHANNEL}__/CSV/{sample}.csv")
