import os, sys
sys.path.insert(0, os.environ['WORKDIR'])
import argparse
from MetaInfo.periodInfo import PeriodDict

from ROOT import TFile
from libPython.Selection import pass_baseline, select
from libPython.DataFormat import get_muons, get_electrons, get_jets
from libPython.DataFormat import Particle
from libPython.DataDriven import FakeEstimator
from libPython.Management import MVAManager
from libPython.HistTools import HistogramWriter

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", "-e", required=True, type=str, help="era")
parser.add_argument("--sample", "-s", default="DoubleMuon",
                    type=str, help="sample name")
args = parser.parse_args()

periodList = PeriodDict[args.era]
try:
    idx = int(args.sample[-1])
    args.sample = args.sample.replace(str(idx), periodList[idx])
    print(args.sample)
except:
    # running full era
    pass

# define event loop
def Loop(evt, fakeEstimator, manager, writer):
    muons = get_muons(evt)
    electrons = get_electrons(evt)
    jets, bjets = get_jets(evt)
    METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)
    
    muons_tight = list(filter(lambda x: x.PassID("tight"), muons))
    electrons_tight = list(filter(lambda x: x.PassID("tight"), electrons))
    
    if not pass_baseline("3Mu", evt, muons, electrons, jets, bjets, "loose"):
        return None
    
    # split into ZGamma & DYJets region
    if muons[0].Pt() < 20. or muons[1].Pt() < 20. or muons[2].Pt() < 20.:
        measure = "DYJets"
    else:
        measure = "ZGamma"
    region = select("3Mu", evt, muons, electrons, jets, bjets, "loose")
    scores = manager.getScores(muons+electrons+jets)
    
    tight_flag = len(muons_tight) == 3 and len(electrons_tight) == 0
    if tight_flag:
        prefix = "3Mu/Baseline/Central/Incl"
        writer.fill_muons(f"{prefix}/muons", muons, 1.)
        writer.fill_electrons(f"{prefix}/electrons", electrons, 1.)
        writer.fill_jets(f"{prefix}/jets", jets, 1.)
        writer.fill_jets(f"{prefix}/bjets", bjets, 1.)
        writer.fill_object(f"{prefix}/METv", METv, 1.)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, 1., 100, 0., 1.)

        prefix = f"3Mu/Baseline/Central/{measure}"
        writer.fill_muons(f"{prefix}/muons", muons, 1.)
        writer.fill_electrons(f"{prefix}/electrons", electrons, 1.)
        writer.fill_jets(f"{prefix}/jets", jets, 1.)
        writer.fill_jets(f"{prefix}/bjets", bjets, 1.)
        writer.fill_object(f"{prefix}/METv", METv, 1.)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, 1., 100, 0., 1.)
    else:
        # Nonprompt
        weight = fakeEstimator.get_fake_weight(muons)
        prefix = "3Mu/Baseline/Nonprompt/Incl"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 100, 0., weight)

        prefix = f"3Mu/Baseline/Nonprompt/{measure}"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 100, 0., 1.) 
        
        # NonpromptUp
        weight = fakeEstimator.get_fake_weight(muons, 1)
        prefix = "3Mu/Baseline/NonpromptUp/Incl"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 100, 0., weight)

        prefix = f"3Mu/Baseline/NonpromptUp/{measure}"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 100, 0., 1.)  
        
        # NonpromptDown
        weight = fakeEstimator.get_fake_weight(muons, -1)
        prefix = "3Mu/Baseline/NonpromptDown/Incl"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 100, 0., weight)

        prefix = f"3Mu/Baseline/NonpromptDown/{measure}"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 100 , 0., 1.) 

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
        
    if tight_flag:
        prefix = f"3Mu/{region}/Central/Incl"
        writer.fill_muons(f"{prefix}/muons", muons, 1.)
        writer.fill_electrons(f"{prefix}/electrons", electrons, 1.)
        writer.fill_jets(f"{prefix}/jets", jets, 1.)
        writer.fill_jets(f"{prefix}/bjets", bjets, 1.)
        writer.fill_object(f"{prefix}/METv", METv, 1.)
        writer.fill_object(f"{prefix}/ZCand", ZCand, 1.)
        writer.fill_object(f"{prefix}/xZCand", xZCand, 1.)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, 1., 1000, 0., 1.)

        prefix = f"3Mu/{region}/Central/{measure}"
        writer.fill_muons(f"{prefix}/muons", muons, 1.)
        writer.fill_electrons(f"{prefix}/electrons", electrons, 1.)
        writer.fill_jets(f"{prefix}/jets", jets, 1.)
        writer.fill_jets(f"{prefix}/bjets", bjets, 1.)
        writer.fill_object(f"{prefix}/METv", METv, 1.)
        writer.fill_object(f"{prefix}/ZCand", ZCand, 1.)
        writer.fill_object(f"{prefix}/xZCand", xZCand, 1.)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, 1., 1000, 0., 1.)
    else:
         # Nonprompt
        weight = fakeEstimator.get_fake_weight(muons)
        prefix = f"3Mu/{region}/Nonprompt/Incl"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., weight)

        prefix = f"3Mu/{region}/Nonprompt/{measure}"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., 1.) 
        
        # NonpromptUp
        weight = fakeEstimator.get_fake_weight(muons, 1)
        prefix = f"3Mu/{region}/NonpromptUp/Incl"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., weight)

        prefix = f"3Mu/{region}/NonpromptUp/{measure}"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., 1.)  
        
        # NonpromptDown
        weight = fakeEstimator.get_fake_weight(muons, -1)
        prefix = f"3Mu/{region}/NonpromptDown/Incl"
        writer.fill_muons(f"{prefix}/muons", muons, weight)
        writer.fill_electrons(f"{prefix}/electrons", electrons, weight)
        writer.fill_jets(f"{prefix}/jets", jets, weight)
        writer.fill_jets(f"{prefix}/bjets", bjets, weight)
        writer.fill_object(f"{prefix}/METv", METv, weight)
        writer.fill_object(f"{prefix}/ZCand", ZCand, weight)
        writer.fill_object(f"{prefix}/xZCand", xZCand, weight)
        for classifier, score in scores.items():
            writer.fill_hist(f"{prefix}/{classifier}/score", score, weight, 1000, 0., weight)

        prefix = f"3Mu/{region}/NonpromptDown/{measure}"
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
    file_path = f"{os.environ['WORKDIR']}/SelectorOutput/{args.era}/Skim3Mu__/DATA/Selector_{args.sample}.root"
    outfile_path = f"{os.environ['WORKDIR']}/triLepRegion/ROOT/Skim3Mu__/{args.era}/{args.sample}.root"
    
    fakeEstimator = FakeEstimator(era=args.era)
    mvaManager = MVAManager()
    histWriter = HistogramWriter(outfile=outfile_path)
    
    f = TFile.Open(file_path)
    for evt in f.Events:
        Loop(evt, fakeEstimator, mvaManager, histWriter)
    f.Close()
    histWriter.close()
