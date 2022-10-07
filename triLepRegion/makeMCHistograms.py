import os, sys; sys.path.insert(0, os.environ['WORKDIR'])
import argparse

from ROOT import TFile
import torch
from libPython.Preprocessor import evt_to_graph
from libPython.Management import predict_proba
from libPython.MLTools import ParticleNet
from libPython.Selection        import pass_baseline, select
from libPython.DataFormat       import get_muons, get_electrons, get_jets
from libPython.DataFormat       import Particle
from libPython.MCCorrection     import MCCorrection
from libPython.HistTools        import HistogramWriter

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", "-e", required=True, type=str, help="era")
parser.add_argument("--sample", "-s", default="DYJets", type=str, help="sample name")
parser.add_argument("--split", action="store_true", default=False, help="Using splitted samples")
args = parser.parse_args()

MASSPOINTs = ["MHc-70_MA-15", "MHc-100_MA-60", "MHc-130_MA-90", "MHc-160_MA-155"]
CLASSIFIERs = ["MHc-70_MA-15_vs_TTLL_powheg", "MHc-70_MA-15_vs_ttX",
               "MHc-100_MA-60_vs_TTLL_powheg",
               "MHc-130_MA_90_vs_TTLL_powheg", "MHc-130_MA-90_vs_ttX",
               "MHc-160_MA-155_vs_TTLL_powheg"]
Systematics = ["Central",
               "L1PrefireUp", "L1PrefireDown",
               "PileUpCorrUp", "PileUpCorrDown",
               "MuonMomentumShiftUp", "MuonMomentumShiftDown",
               "JetEnShiftUp", "JetEnShiftDown",
               "JetResShiftUp", "JetResShiftDown",
               "MuonIDSFUp", "MuonIDSFDown",
               "DblMuonTrigSFUp", "DblMuonTrigSFDown"
               ]

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

def Loop(evt, classifiers, mcCorr, syst, writer):
    muonMomentumShift = 0
    if syst == "MuonMomentumShiftUp":
        muonMomentumShift = 1
    if syst == "MuonMomentumShiftDown":
        muonMomentumShift = -1
    
    electronEnShift = 0
    electronResShift = 0
    
    jetEnShift = 0
    if syst == "JetEnShiftUp":
        jetEnShift = 1
    if syst == "JetEnShiftDown":
        jetEnShift = -1
    
    jetResShift = 0
    if syst == "JetResShiftUp":
        jetResShift = 1
    if syst == "jetResShiftDown":
        jetResShift = -1
        
    muons = get_muons(evt, muonMomentumShift)
    electrons = get_electrons(evt, electronEnShift, electronResShift)
    jets, bjets = get_jets(evt, jetEnShift, jetResShift)
    METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)
    objects = muons+electrons+jets; objects.append(METv)
    
    if not pass_baseline("3Mu", evt, muons, electrons, jets, bjets, "tight"):
        return None
    
    # prompt matching
    if not len(list(filter(lambda x: x.LepType() > 0, muons))) == 3:
        return None
    if not len(list(filter(lambda x: x.LepType() > 0, electrons))) == 0:
        return None
    
    #region
    region = select("3Mu", evt, muons, electrons, jets, bjets, "tight")
    #measure
    if muons[0].Pt() < 20. or muons[1].Pt() < 20. or muons[2].Pt() < 20.:
        measure = "DYJets"
    else:
        measure = "ZGamma"
        
    ZCand, xZCand = makeACand(muons, mA=91.2)
        
    systPrefire = 0
    systPileup = 0
    systMuonIDSF = 0
    systMuonTrigSF = 0
    if syst == "L1PrefireUp":       systPrefire = 1
    if syst == "L1PrefireDown":     systPrefire = -1
    if syst == "PileupCorrUp":      systPileup = 1
    if syst == "PileupCorrDown":    systPileup = -1
    if syst == "MuonIDSFUp":        systMuonIDSF = 1
    if syst == "MuonIDSFDown":      systMuonIDSF = -1
    if syst == "DblMuonTrigSFUp":   systMuonTrigSF = 1
    if syst == "DblMuonTrigSFDown": systMuonTrigSF = -1
    
    weight = evt.GenWeight * evt.TrigLumi
    weight *= mcCorr.GetL1PrefireWeight(evt, systPrefire)
    weight *= mcCorr.GetPileupWeight(evt.nPileUp, systPileup)
    weight *= mcCorr.GetMuonIDSF(muons, systMuonIDSF)
    weight *= mcCorr.GetDblMuonTriggerSF(muons, systMuonTrigSF)
    weight *= mcCorr.GetBtaggingWeight(jets)
    
    # fill baseline
    prefix = f"3Mu/Baseline/{syst}/Incl/Inputs"
    writer.fill_muons(f"{prefix}/muons", muons, weight)
    writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
    writer.fill_jets(f"{prefix}/jets", jets, weight)
    writer.fill_jets(f"{prefix}/bjets", bjets, weight)
    writer.fill_object(f"{prefix}/METv", METv, weight)
    writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
    writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
    
    prefix = f"3Mu/Baseline/{syst}/{measure}/Inputs"
    writer.fill_muons(f"{prefix}/muons", muons, weight)
    writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
    writer.fill_jets(f"{prefix}/jets", jets, weight)
    writer.fill_jets(f"{prefix}/bjets", bjets, weight)
    writer.fill_object(f"{prefix}/METv", METv, weight)
    writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
    writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
    
    prefix = f"3Mu/Baseline/{syst}/Incl/Outputs"
    for mp in MASSPOINTs:
        mA = mp.split("_")[1]
        mA = int(mA.split("-")[1])
        ACand, xACand = makeACand(muons, mA)
        score_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
        score_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
        writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_TTLL_powheg, weight, 100, 0., 1.)
        writer.fill_hist(f"{prefix}/{mp}/score_ttX", score_ttX, weight, 100, 0., 1.)
        writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
        writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
        writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
        writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_ttX, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
    
    prefix = f"3Mu/Baseline/{syst}/{measure}/Outputs"
    for mp in MASSPOINTs:
        mA = mp.split("_")[1]
        mA = int(mA.split("-")[1])
        ACand, xACand = makeACand(muons, mA)
        score_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
        score_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
        writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_TTLL_powheg, weight, 100, 0., 1.)
        writer.fill_hist(f"{prefix}/{mp}/score_ttX", score_ttX, weight, 100, 0., 1.)
        writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
        writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
        writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
        writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_ttX, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
        
    # Signal / Control Region
    if region is None:
        return None
    if region == "ZGammaRegion":
        ZCand = muons[0]+muons[1]+muons[2]
        xZCand = Particle(0., 0., 0., 0.)
    
    prefix = f"3Mu/{region}/{syst}/Incl/Inputs"
    writer.fill_muons(f"{prefix}/muons", muons, weight)
    writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
    writer.fill_jets(f"{prefix}/jets", jets, weight)
    writer.fill_jets(f"{prefix}/bjets", bjets, weight)
    writer.fill_object(f"{prefix}/METv", METv, weight)
    writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
    writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
    
    prefix = f"3Mu/{region}/{syst}/{measure}/Inputs"
    writer.fill_muons(f"{prefix}/muons", muons, weight)
    writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
    writer.fill_jets(f"{prefix}/jets", jets, weight)
    writer.fill_jets(f"{prefix}/bjets", bjets, weight)
    writer.fill_object(f"{prefix}/METv", METv, weight)
    writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
    writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
    
    prefix = f"3Mu/{region}/{syst}/Incl/Outputs"
    for mp in MASSPOINTs:
        mA = mp.split("_")[1]
        mA = int(mA.split("-")[1])
        ACand, xACand = makeACand(muons, mA)
        score_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
        score_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
        writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_TTLL_powheg, weight, 100, 0., 1.)
        writer.fill_hist(f"{prefix}/{mp}/score_ttX", score_ttX, weight, 100, 0., 1.)
        writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
        writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
        writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
        writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_ttX, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
    
    prefix = f"3Mu/{region}/{syst}/{measure}/Outputs"
    for mp in MASSPOINTs:
        mA = mp.split("_")[1]
        mA = int(mA.split("-")[1])
        ACand, xACand = makeACand(muons, mA)
        score_TTLL_powheg = getScore(classifiers[f"{mp}_vs_TTLL_powheg"], objects)
        score_ttX = getScore(classifiers[f"{mp}_vs_ttX"], objects)
        writer.fill_hist(f"{prefix}/{mp}/score_vs_TTLL_powheg", score_TTLL_powheg, weight, 100, 0., 1.)
        writer.fill_hist(f"{prefix}/{mp}/score_ttX", score_ttX, weight, 100, 0., 1.)
        writer.fill_object(f"{prefix}/{mp}/ACand", ACand, weight)
        writer.fill_object(f"{prefix}/{mp}/xACand", xACand, weight)
        writer.fill_hist2d(f"{prefix}/{mp}/score_vs_TTLL_powheg_mACand", score_TTLL_powheg, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)
        writer.fill_hist2d(f"{prefix}/{mp}/score_vs_ttX_mACand", score_ttX, ACand.M(), weight, 100, 0., 1., 1000, 0., 1000.)

if __name__ == "__main__":
    file_path = f"{os.environ['WORKDIR']}/SelectorOutput/{args.era}/Skim3Mu__"
    if args.split:
        file_path += "/Split"
    file_path += f"/Selector_{args.sample}.root"
    outfile_path = f"{os.environ['WORKDIR']}/triLepRegion/ROOT/Skim3Mu__/{args.era}/{args.sample}.root"
    
    mcCorr = MCCorrection(era=args.era)
    mcCorr.SetBtaggingHandler(tagger="DeepJet", wp="Medium", syst="central")
    histWriter = HistogramWriter(outfile=outfile_path)
    
    # load classifiers
    optimizers = {"MHc-70_MA-15_vs_TTLL_powheg": "AdamW",
                  "MHc-70_MA-15_vs_ttX": "Adam",
                  "MHc-100_MA-60_vs_TTLL_powheg": "Adam",
                  "MHc-130_MA-90_vs_TTLL_powheg": "AdamW",
                  "MHc-130_MA-90_vs_ttX": "RMSprop",
                  "MHc-160_MA-155_vs_TTLL_powheg": "AdamW"}
    initLRs =    {"MHc-70_MA-15_vs_TTLL_powheg": 0.002,
                  "MHc-70_MA-15_vs_ttX": 0.02,
                  "MHc-100_MA-60_vs_TTLL_powheg": 0.01,
                  "MHc-130_MA-90_vs_TTLL_powheg": 0.01,
                  "MHc-130_MA-90_vs_ttX": 0.001,
                  "MHc-160_MA-155_vs_TTLL_powheg": 2e-05}
    schedulers = {"MHc-70_MA-15_vs_TTLL_powheg": "StepLR",
                  "MHc-70_MA-15_vs_ttX": "ExponentialLR",
                  "MHc-100_MA-60_vs_TTLL_powheg": "ExponentialLR",
                  "MHc-130_MA-90_vs_TTLL_powheg": "ExponentialLR",
                  "MHc-130_MA-90_vs_TTLL_powheg": "ExponentialLR",
                  "MHc-160_MA-155_vs_TTLL_powheg": "ExponentialLR"}
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
        for syst in Systematics:
            Loop(evt, classifiers, mcCorr, syst, histWriter)
    f.Close()
    histWriter.close()
    del classifiers
