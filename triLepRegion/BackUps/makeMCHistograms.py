import os, sys
sys.path.insert(0, os.environ['WORKDIR'])
import argparse

from ROOT import TFile
from libPython.Selection        import pass_baseline, select
from libPython.DataFormat       import get_muons, get_electrons, get_jets
from libPython.DataFormat       import Particle
from libPython.MCCorrection     import MCCorrection
from libPython.Management       import MVAManager
from libPython.HistTools        import HistogramWriter

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", "-e", required=True, type=str, help="era")
parser.add_argument("--sample", "-s", default="DYJets", type=str, help="sample name")
parser.add_argument("--split", action="store_true", default=False, help="Using splitted samples")
args = parser.parse_args()

Systematics = ["Central",
               "L1PrefireUp", "L1PrefireDown",
               "PileUpCorrUp", "PileUpCorrDown",
               "MuonMomentumShiftUp", "MuonMomentumShiftDown",
               "JetEnShiftUp", "JetEnShiftDown",
               "JetResShiftUp", "JetResShiftDown",
               "MuonIDSFUp", "MuonIDSFDown",
               "DblMuonTrigSFUp", "DblMuonTrigSFDown"]

def Loop(evt, manager, mcCorr, syst, writer):
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
    
    if not pass_baseline("3Mu", evt, muons, electrons, jets, bjets, "tight"):
        return None
    
    # prompt matching
    if not len(list(filter(lambda x: x.LepType() > 0, muons))) == 3:
        return None
    if not len(list(filter(lambda x: x.LepType() > 0, electrons))) == 0:
        return None
    
    region = select("3Mu", evt, muons, electrons, jets, bjets, "tight")
    scores = manager.getScores(muons+electrons+jets)
    
    if muons[0].Pt() < 20. or muons[1].Pt() < 20. or muons[2].Pt() < 20.:
        measure = "DYJets"
    else:
        measure = "ZGamma"
        
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
    prefix = f"3Mu/Baseline/{syst}/Incl"
    writer.fill_muons(f"{prefix}/muons", muons, weight)
    writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
    writer.fill_jets(f"{prefix}/jets", jets, weight)
    writer.fill_jets(f"{prefix}/bjets", bjets, weight)
    writer.fill_object(f"{prefix}/METv", METv, weight)
    for classifier, score in scores.items():
        writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., 1.)
    
    prefix = f"3Mu/Baseline/{syst}/{measure}"
    writer.fill_muons(f"{prefix}/muons", muons, weight)
    writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
    writer.fill_jets(f"{prefix}/jets", jets, weight)
    writer.fill_jets(f"{prefix}/bjets", bjets, weight)
    writer.fill_object(f"{prefix}/METv", METv, weight)
    for classifier, score in scores.items():
        writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., 1.)

    # Signal / Control regions    
    if region is None:
        return None
    
    ZCand = Particle(0., 0., 0., 0.)
    xZCand = Particle(0., 0., 0., 0.)
    if region == "ZFakeRegion":
        mZ = 91.2
        # make os pair
        if abs(muons[0].Charge() + muons[1].Charge()) == 2:
            pair1 = muons[0] + muons[2]
            pair2 = muons[1] + muons[2]
        elif abs(muons[0].Charge() + muons[2].Charge()) == 2:
            pair1 = muons[0] + muons[1]
            pair2 = muons[1] + muons[2]
        else:   # 1 == 2
            pair1 = muons[0] + muons[1]
            pair2 = muons[0] + muons[2]

        if abs(pair1.M() - mZ) < abs(pair2.M() - mZ):
            ZCand, xZCand = pair1, pair2
        else:
            ZCand, xZCand = pair2, pair1
    if region == "ZGammaRegion":
        ZCand = muons[0] + muons[1] + muons[2]
        
    prefix = f"3Mu/{region}/{syst}/Incl"
    writer.fill_muons(f"{prefix}/muons", muons, weight)
    writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
    writer.fill_jets(f"{prefix}/jets", jets, weight)
    writer.fill_jets(f"{prefix}/bjets", bjets, weight)
    writer.fill_object(f"{prefix}/METv", METv, weight)
    writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
    writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
    for classifier, score in scores.items():
        writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., 1.)
    
    prefix = f"3Mu/{region}/{syst}/{measure}"
    writer.fill_muons(f"{prefix}/muons", muons, weight)
    writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
    writer.fill_jets(f"{prefix}/jets", jets, weight)
    writer.fill_jets(f"{prefix}/bjets", bjets, weight)
    writer.fill_object(f"{prefix}/METv", METv, weight)
    writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
    writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
    for classifier, score in scores.items():
        writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., 1.)
    
if __name__ == "__main__":
    file_path = f"{os.environ['WORKDIR']}/SelectorOutput/{args.era}/Skim3Mu__"
    if args.split:
        file_path += "/Split"
    file_path += f"/Selector_{args.sample}.root"
    outfile_path = f"{os.environ['WORKDIR']}/triLepRegion/ROOT/Skim3Mu__/{args.era}/{args.sample}.root"
    
    mvaManager = MVAManager()
    mcCorr = MCCorrection(era=args.era)
    mcCorr.SetBtaggingHandler(tagger="DeepJet", wp="Medium", syst="central")
    histWriter = HistogramWriter(outfile=outfile_path)
    
    f = TFile.Open(file_path)
    for evt in f.Events:
        for syst in Systematics:
            Loop(evt, mvaManager, mcCorr, syst, histWriter)
    f.Close()
    histWriter.close()
