import os, sys; sys.path.insert(0, os.environ['WORKDIR'])
import argparse
from MetaInfo.AllEras import PeriodDict

from ROOT import TFile
import torch
from libPython.Preprocessor import evt_to_graph
from libPython.Management import predict_proba
from libPython.MLTools import ParticleNet
from libPython.Selection import pass_baseline, select
from libPython.DataFormat import get_muons, get_electrons, get_jets
from libPython.DataFormat import Particle
from libPython.DataDriven import FakeEstimator
from libPython.HistTools import HistogramWriter

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", "-e", required=True, type=str, help="era")
parser.add_argument("--sample", "-s", default="DoubleMuon", type=str, help="sample name")
args = parser.parse_args()

# to submit to condor
# override idx to data period
# e.g. for 2016preVFP, DoubleMuon_0 -> DoubleMuon_B_ver2
periodList = PeriodDict[args.era]
idx = int(args.sample[-1])
args.sample = args.sample.replace(str(idx), periodList[idx])
MASSPOINTs = ["MHc-70_MA-15", "MHc-100_MA-60", "MHc-130_MA-90", "MHc-160_MA-155"]
CLASSIFIERs = ["MHc-70_MA-15_vs_TTLL_powheg", "MHc-70_MA-15_vs_ttX",
               "MHc-100_MA-60_vs_TTLL_powheg", "MHc-100_MA-60_vs_ttX",
               "MHc-130_MA-90_vs_TTLL_powheg", "MHc-130_MA-90_vs_ttX",
               "MHc-160_MA-155_vs_TTLL_powheg", "MHc-160_MA-155_vs_ttX"]

def getScore(model, objects):
    model.eval()
    node_list = []
    for obj in objects:
        node_list.append([obj.Pt(),
                          obj.Eta(),
                          obj.Phi(),
                          obj.M(),
                          obj.Charge(),
                          obj.IsMuon(),
                          obj.IsElectron(),
                          obj.IsJet(),
                          obj.BtagScore()])
    data = evt_to_graph(node_list, y=None, k=4)
    return predict_proba(model, data.x, data.edge_index)

def makeACand(muons, mA):
    ACand = Particle(0., 0., 0., 0.)
    xACand = Particle(0., 0., 0., 0.)
    # make pairs
    if abs(muons[0].Charge() + muons[1].Charge()) == 2:
        pair1 = muons[0] + muons[2]
        pair2 = muons[1] + muons[2]
    elif abs(muons[0].Charge() + muons[2].Charge()) == 2:
        pair1 = muons[0] + muons[1]
        pair2 = muons[1] + muons[2]
    else:   # 1 == 2
        pair1 = muons[0] + muons[1]
        pair2 = muons[0] + muons[2]
        
    if abs(pair1.M() - mA) < abs(pair2.M() - mA):
        ACand, xACand = pair1, pair2
    else:
        ACand, xACand = pair2, pair1
    return (ACand, xACand)

# define event loop
def Loop(evt, fakeEstimator, classifiers, writer):
    muons = get_muons(evt)
    electrons = get_electrons(evt)
    jets, bjets = get_jets(evt)
    METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)
    objects = muons+electrons+jets; objects.append(METv)
            
    muons_tight = list(filter(lambda x: x.PassID("tight"), muons))
    electrons_tight = list(filter(lambda x: x.PassID("tight"), electrons))

    if not pass_baseline("3Mu", evt, muons, electrons, jets, bjets, "loose"):
        return None
    region = select("3Mu", evt, muons, electrons, jets, bjets, "loose")
    
    # measure
    measure = ""
    if muons[0].Pt() < 20. or muons[1].Pt() < 20. or muons[2].Pt() < 20.:
        measure = "DYJets"
    else:
        measure = "ZGamma"
    
    tight_flag= len(muons_tight) == 3 and len(electrons_tight) == 0
    ZCand, xZCand = makeACand(muons, mA=91.2)
    
    if tight_flag:
        prefix = "3Mu/Baseline/Central/Incl/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, 1.)
        writer.fill_electrons(f"{prefix}/electrons", electrons, 1.)
        writer.fill_jets(f"{prefix}/jets", jets, 1.)
        writer.fill_jets(f"{prefix}/bjets", bjets, 1.)
        writer.fill_object(f"{prefix}/METv", METv, 1.)
        writer.fill_object(f"{prefix}/ZCand", ZCand, 1.)
        writer.fill_object(f"{prefix}/xZCand", xZCand, 1.)
        
        prefix = f"3Mu/Baseline/Central/{measure}/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, 1.)
        writer.fill_electrons(f"{prefix}/electrons", electrons, 1.)
        writer.fill_jets(f"{prefix}/jets", jets, 1.)
        writer.fill_jets(f"{prefix}/bjets", bjets, 1.)
        writer.fill_object(f"{prefix}/METv", METv, 1.)
        writer.fill_object(f"{prefix}/ZCand", ZCand, 1.)
        writer.fill_object(f"{prefix}/xZCand", xZCand, 1.)
        
        prefix = "3Mu/Baseline/Central/Incl/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, 1., 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, 1., 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, 1.)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, 1.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), 1., 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), 1., 100, 0., 1.,1000, 0., 1000.)
            
        prefix = f"3Mu/Baseline/Central/{measure}/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, 1., 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, 1., 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, 1.)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, 1.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), 1., 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), 1., 100, 0., 1.,1000, 0., 1000.)
    else:
        # Nonprompt
        weight = fakeEstimator.get_fake_weight(muons) 
        prefix = "3Mu/Baseline/Nonprompt/Incl/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
         
        
        prefix = f"3Mu/Baseline/Nonprompt/{measure}/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = "3Mu/Baseline/Nonprompt/Incl/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
        
        prefix = f"3Mu/Baseline/Nonprompt/{measure}/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
            
        # NonpromptUp
        weight = fakeEstimator.get_fake_weight(muons, 1) 
        prefix = "3Mu/Baseline/NonpromptUp/Incl/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight) 
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = f"3Mu/Baseline/NonpromptUp/{measure}/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = "3Mu/Baseline/NonpromptUp/Incl/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
        
        prefix = f"3Mu/Baseline/NonpromptUp/{measure}/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
            
        # NonpromptDown
        weight = fakeEstimator.get_fake_weight(muons, -1) 
        prefix = "3Mu/Baseline/NonpromptDown/Incl/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight) 
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = f"3Mu/Baseline/NonpromptDown/{measure}/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = "3Mu/Baseline/NonpromptDown/Incl/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
        
        prefix = f"3Mu/Baseline/NonpromptDown/{measure}/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
            
    if region is None:
        return None
    
    if region == "ZGammaRegion":
        ZCand = muons[0]+muons[1]+muons[2]
        xZCand = Particle(0., 0., 0., 0)
        
    if tight_flag:
        prefix = f"3Mu/{region}/Central/Incl/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, 1.)
        writer.fill_electrons(f"{prefix}/electrons", electrons, 1.)
        writer.fill_jets(f"{prefix}/jets", jets, 1.)
        writer.fill_jets(f"{prefix}/bjets", bjets, 1.)
        writer.fill_object(f"{prefix}/METv", METv, 1.)
        writer.fill_object(f"{prefix}/ZCand", ZCand, 1.)
        writer.fill_object(f"{prefix}/xZCand", xZCand, 1.)
        
        prefix = f"3Mu/{region}/Central/{measure}/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, 1.)
        writer.fill_electrons(f"{prefix}/electrons", electrons, 1.)
        writer.fill_jets(f"{prefix}/jets", jets, 1.)
        writer.fill_jets(f"{prefix}/bjets", bjets, 1.)
        writer.fill_object(f"{prefix}/METv", METv, 1.)
        writer.fill_object(f"{prefix}/ZCand", ZCand, 1.)
        writer.fill_object(f"{prefix}/xZCand", xZCand, 1.)
        
        prefix = f"3Mu/{region}/Central/Incl/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, 1., 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, 1., 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, 1.)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, 1.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), 1., 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), 1., 100, 0., 1.,1000, 0., 1000.)
            
        prefix = f"3Mu/{region}/Central/{measure}/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, 1., 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, 1., 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, 1.)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, 1.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), 1., 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), 1., 100, 0., 1.,1000, 0., 1000.)
    else:
        # Nonprompt
        weight = fakeEstimator.get_fake_weight(muons) 
        prefix = f"3Mu/{region}/Nonprompt/Incl/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight) 
        
        prefix = f"3Mu/{region}/Nonprompt/{measure}/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = f"3Mu/{region}/Nonprompt/Incl/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
        
        prefix = f"3Mu/{region}/Nonprompt/{measure}/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
            
        # NonpromptUp
        weight = fakeEstimator.get_fake_weight(muons, 1) 
        prefix = f"3Mu/{region}/NonpromptUp/Incl/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight) 
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = f"3Mu/{region}/NonpromptUp/{measure}/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = f"3Mu/{region}/NonpromptUp/Incl/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
        
        prefix = f"3Mu/{region}/NonpromptUp/{measure}/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
                
        # NonpromptDown
        weight = fakeEstimator.get_fake_weight(muons, -1) 
        prefix = f"3Mu/{region}/NonpromptDown/Incl/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight) 
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = f"3Mu/{region}/NonpromptDown/{measure}/Inputs"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        
        prefix = f"3Mu/{region}/NonpromptDown/Incl/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
            
        prefix = f"3Mu/{region}/NonpromptDown/{measure}/Outputs"
        for mp in MASSPOINTs:
            mA = mp.split("_")[1]
            mA = int(mA.split("-")[1])
            ACand, xACand = makeACand(muons, mA)
            score_vs_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
            score_vs_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_vs_TTLL_powheg, weight, 100, 0., 1.)
            writer.fill_hist(f"{prefix}/{mp}/score_vs_ttX", score_vs_ttX, weight, 100, 0., 1.)
            writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
            writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_vs_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
            writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_vs_ttX, ACand.M(), weight, 100, 0., 1.,1000, 0., 1000.)
            
if __name__ == "__main__":
    file_path = f"{os.environ['WORKDIR']}/SelectorOutput/{args.era}/Skim3Mu__/DATA/Selector_{args.sample}.root"
    outfile_path = f"{os.environ['WORKDIR']}/triLepRegion/ROOT/Skim3Mu__/{args.era}/{args.sample}.root"
    
    fakeEstimator = FakeEstimator(era=args.era)
    histWriter = HistogramWriter(outfile=outfile_path)
    
    # load classifiers
    optimizers = {"MHc-70_MA-15_vs_TTLL_powheg":   "AdamW",
                  "MHc-70_MA-15_vs_ttX":           "AdamW",
                  "MHc-100_MA-60_vs_TTLL_powheg":  "Adam",
                  "MHc-100_MA-60_vs_ttX":          "Adam",
                  "MHc-130_MA-90_vs_TTLL_powheg":  "AdamW",
                  "MHc-130_MA-90_vs_ttX":          "RMSprop",
                  "MHc-160_MA-155_vs_TTLL_powheg": "AdamW",
                  "MHc-160_MA-155_vs_ttX":         "Adam"}
    initLRs =    {"MHc-70_MA-15_vs_TTLL_powheg":   "0.01",
                  "MHc-70_MA-15_vs_ttX":           "0.005",
                  "MHc-100_MA-60_vs_TTLL_powheg":  "0.01",
                  "MHc-100_MA-60_vs_ttX":          "1e-05",
                  "MHc-130_MA-90_vs_TTLL_powheg":  "0.005",
                  "MHc-130_MA-90_vs_ttX":          "0.0002",
                  "MHc-160_MA-155_vs_TTLL_powheg": "0.01",
                  "MHc-160_MA-155_vs_ttX":         "0.01"}
    schedulers = {"MHc-70_MA-15_vs_TTLL_powheg":   "ExponentialLR",
                  "MHc-70_MA-15_vs_ttX":           "StepLR",
                  "MHc-100_MA-60_vs_TTLL_powheg":  "StepLR",
                  "MHc-100_MA-60_vs_ttX":          "StepLR",
                  "MHc-130_MA-90_vs_TTLL_powheg":  "StepLR",
                  "MHc-130_MA-90_vs_ttX":          "ExponentialLR",
                  "MHc-160_MA-155_vs_TTLL_powheg": "ExponentialLR",
                  "MHc-160_MA-155_vs_ttX":         "ExponentialLR"}
    classifiers = {}
    for classifier in CLASSIFIERs:
        optim = optimizers[classifier]
        initLR = initLRs[classifier]
        scheduler = schedulers[classifier]
        model_path = f"{os.environ['WORKDIR']}/models/full/{classifier}/ParticleNet_{optim}_initLR-{str(initLR).replace('.', 'p')}_{scheduler}.pt"
        classifiers[classifier] = ParticleNet(num_features=9, num_classes=2, hidden_channels=128)
        classifiers[classifier].load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    
    f = TFile.Open(file_path)
    for evt in f.Events:
        Loop(evt, fakeEstimator, classifiers, histWriter)
    f.Close()
    histWriter.close()
    del classifiers
