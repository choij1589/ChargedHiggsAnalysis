import os; os.environ['WORKDIR'] = "/home/choij/workspace/ChargedHiggsAnalysis"
import sys; sys.path.insert(0, os.environ['WORKDIR'])

from libPython.HistTools import HistogramWriter
from libPython.MCCorrection import MCCorrection
from libPython.DataDriven import FakeEstimator, Conversion
from libPython.Selection import pass_baseline, select
from libPython.DataFormat import get_muons, get_electrons, get_jets
from libPython.DataFormat import Particle
from ROOT import TFile
import argparse

# Set up
parser = argparse.ArgumentParser()
parser.add_argument("--era", "-e", default="2017", type=str, help="era")
parser.add_argument("--sample", "-s", default="DYJets",
                    type=str, help="sample name")
parser.add_argument("--isData", "-d", action="store_true",
                    default=False, help="DATA or MC")
parser.add_argument("--scaleConv", "-c", action="store_true",
                    default=False, help="scale conversion samples or not")
args = parser.parse_args()

Systematics = ["Central",
               "L1PrefireUp", "L1PrefireDown",
               "PileUpCorrUp", "PileUpCorrDown",
               "MuonMomentumShiftUp", "MuonMomentumShiftDown",
               "JetEnShiftUp", "JetEnShiftDown",
               "JetResShiftUp", "JetResShiftDown",
               "MuonIDSFUp", "MuonIDSFDown",
               "DblMuonTrigSFUp", "DblMuonTrigSFDown"]

if args.sample in ["DYJets", "ZGToLLG"] and args.scaleConv:
    Systematics = ["Central",
                   "ConversionUp", "ConversionDown"]

# Loops


def DataLoop(evt, writer, fakeEstimator):
    muons = get_muons(evt)
    electrons = get_electrons(evt)
    jets, bjets = get_jets(evt)
    METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)

    muons_tight = list(filter(lambda x: x.PassID("tight"), muons))
    electrons_tight = list(filter(lambda x: x.PassID("tight"), electrons))

    if not pass_baseline("3Mu", evt, muons, electrons, jets, bjets, "loose"):
        return None

    if muons[0].Pt() < 20. or muons[1].Pt() < 20. or muons[2].Pt() < 20.:
        measure = "DYJets"
    else:
        measure = "ZGamma"

    if len(muons_tight) == 3 and len(electrons_tight) == 0:
        writer.fill_muons(f"3Mu/Baseline/Central/muons", muons, 1.)
        writer.fill_electrons(f"3Mu/Baseline/Central/electrons", electrons, 1.)
        writer.fill_jets(f"3Mu/Baseline/Central/jets", jets, 1.)
        writer.fill_jets(f"3Mu/Baseline/Central/bjets", bjets, 1.)
        writer.fill_object(f"3Mu/Baseline/Central/METv", METv, 1.)

        writer.fill_muons(f"3Mu/Baseline/Central/{measure}/muons", muons, 1.)
        writer.fill_electrons(
            f"3Mu/Baseline/Central/{measure}/electrons", electrons, 1.)
        writer.fill_jets(f"3Mu/Baseline/Central/{measure}/jets", jets, 1.)
        writer.fill_jets(f"3Mu/Baseline/Central/{measure}/bjets", bjets, 1.)
        writer.fill_object(f"3Mu/Baseline/Central/{measure}/METv", METv, 1.)
    else:
        weight = fakeEstimator.get_fake_weight(muons)
        writer.fill_muons(f"3Mu/Baseline/Nonprompt/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/Baseline/Nonprompt/electrons", electrons, weight)
        writer.fill_jets(f"3Mu/Baseline/Nonprompt/jets", jets, weight)
        writer.fill_jets(f"3Mu/Baseline/Nonprompt/bjets", bjets, weight)
        writer.fill_object(f"3Mu/Baseline/Nonprompt/METv", METv, weight)

        writer.fill_muons(
            f"3Mu/Baseline/Nonprompt/{measure}/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/Baseline/Nonprompt/{measure}/electrons", electrons, weight)
        writer.fill_jets(
            f"3Mu/Baseline/Nonprompt/{measure}/jets", jets, weight)
        writer.fill_jets(
            f"3Mu/Baseline/Nonprompt/{measure}/bjets", bjets, weight)
        writer.fill_object(
            f"3Mu/Baseline/Nonprompt/{measure}/METv", METv, weight)

        weight = fakeEstimator.get_fake_weight(muons, 1)
        writer.fill_muons(f"3Mu/Baseline/NonpromptUp/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/Baseline/NonpromptUp/electrons", electrons, weight)
        writer.fill_jets(f"3Mu/Baseline/NonpromptUp/jets", jets, weight)
        writer.fill_jets(f"3Mu/Baseline/NonpromptUp/bjets", bjets, weight)
        writer.fill_object(f"3Mu/Baseline/NonpromptUp/METv", METv, weight)

        writer.fill_muons(
            f"3Mu/Baseline/NonpromptUp/{measure}/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/Baseline/NonpromptUp/{measure}/electrons", electrons, weight)
        writer.fill_jets(
            f"3Mu/Baseline/NonpromptUp/{measure}/jets", jets, weight)
        writer.fill_jets(
            f"3Mu/Baseline/NonpromptUp/{measure}/bjets", bjets, weight)
        writer.fill_object(
            f"3Mu/Baseline/NonpromptUp/{measure}/METv", METv, weight)

        weight = fakeEstimator.get_fake_weight(muons, -1)
        writer.fill_muons(f"3Mu/Baseline/NonpromptDown/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/Baseline/NonpromptDown/electrons", electrons, weight)
        writer.fill_jets(f"3Mu/Baseline/NonpromptDown/jets", jets, weight)
        writer.fill_jets(f"3Mu/Baseline/NonpromptDown/bjets", bjets, weight)
        writer.fill_object(f"3Mu/Baseline/NonpromptDown/METv", METv, weight)

        writer.fill_muons(
            f"3Mu/Baseline/NonpromptDown/{measure}/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/Baseline/NonpromptDown/{measure}/electrons", electrons, weight)
        writer.fill_jets(
            f"3Mu/Baseline/NonpromptDown/{measure}/jets", jets, weight)
        writer.fill_jets(
            f"3Mu/Baseline/NonpromptDown/{measure}/bjets", bjets, weight)
        writer.fill_object(
            f"3Mu/Baseline/NonpromptDown/{measure}/METv", METv, weight)

    region = select("3Mu", evt, muons, electrons, jets, bjets, "loose")
    if not region:
        return None

    ZCand = Particle(0., 0., 0., 0)
    xZCand = Particle(0., 0., 0., 0)
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

    if len(muons_tight) == 3:
        writer.fill_muons(f"3Mu/{region}/Central/Incl/muons", muons, 1.)
        writer.fill_electrons(
            f"3Mu/{region}/Central/Incl/electrons", electrons, 1.)
        writer.fill_jets(f"3Mu/{region}/Central/Incl/jets", jets, 1.)
        writer.fill_jets(f"3Mu/{region}/Central/Incl/bjets", bjets, 1.)
        writer.fill_object(f"3Mu/{region}/Central/Incl/METv", METv, 1.)
        writer.fill_object(f"3Mu/{region}/Central/Incl/ZCand", ZCand, 1.)
        writer.fill_object(f"3Mu/{region}/Central/Incl/xZCand", xZCand, 1.)

        writer.fill_muons(f"3Mu/{region}/Central/{measure}/muons", muons, 1.)
        writer.fill_electrons(
            f"3Mu/{region}/Central/{measure}/electrons", electrons, 1.)
        writer.fill_jets(f"3Mu/{region}/Central/{measure}/jets", jets, 1.)
        writer.fill_jets(f"3Mu/{region}/Central/{measure}/bjets", bjets, 1.)
        writer.fill_object(f"3Mu/{region}/Central/{measure}/METv", METv, 1.)
        writer.fill_object(f"3Mu/{region}/Central/{measure}/ZCand", ZCand, 1.)
        writer.fill_object(
            f"3Mu/{region}/Central/{measure}/xZCand", xZCand, 1.)
    else:
        weight = fakeEstimator.get_fake_weight(muons)
        writer.fill_muons(f"3Mu/{region}/Nonprompt/Incl/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/{region}/Nonprompt/Incl/electrons", electrons, weight)
        writer.fill_jets(f"3Mu/{region}/Nonprompt/Incl/jets", jets, weight)
        writer.fill_jets(f"3Mu/{region}/Nonprompt/Incl/bjets", bjets, weight)
        writer.fill_object(f"3Mu/{region}/Nonprompt/Incl/METv", METv, weight)
        writer.fill_object(f"3Mu/{region}/Nonprompt/Incl/ZCand", ZCand, weight)
        writer.fill_object(
            f"3Mu/{region}/Nonprompt/Incl/xZCand", xZCand, weight)

        writer.fill_muons(
            f"3Mu/{region}/Nonprompt/{measure}/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/{region}/Nonprompt/{measure}/electrons", electrons, weight)
        writer.fill_jets(
            f"3Mu/{region}/Nonprompt/{measure}/jets", jets, weight)
        writer.fill_jets(
            f"3Mu/{region}/Nonprompt/{measure}/bjets", bjets, weight)
        writer.fill_object(
            f"3Mu/{region}/Nonprompt/{measure}/METv", METv, weight)
        writer.fill_object(
            f"3Mu/{region}/Nonprompt/{measure}/ZCand", ZCand, weight)
        writer.fill_object(
            f"3Mu/{region}/Nonprompt/{measure}/xZCand", xZCand, weight)

        weight = fakeEstimator.get_fake_weight(muons, 1)
        writer.fill_muons(
            f"3Mu/{region}/NonpromptUp/Incl/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/{region}/NonpromptUp/Incl/electrons", electrons, weight)
        writer.fill_jets(f"3Mu/{region}/NonpromptUp/Incl/jets", jets, weight)
        writer.fill_jets(f"3Mu/{region}/NonpromptUp/Incl/bjets", bjets, weight)
        writer.fill_object(f"3Mu/{region}/NonpromptUp/Incl/METv", METv, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptUp/Incl/ZCand", ZCand, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptUp/Incl/xZCand", xZCand, weight)

        writer.fill_muons(
            f"3Mu/{region}/NonpromptUp/{measure}/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/{region}/NonpromptUp/{measure}/electrons", electrons, weight)
        writer.fill_jets(
            f"3Mu/{region}/NonpromptUp/{measure}/jets", jets, weight)
        writer.fill_jets(
            f"3Mu/{region}/NonpromptUp/{measure}/bjets", bjets, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptUp/{measure}/METv", METv, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptUp/{measure}/ZCand", ZCand, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptUp/{measure}/xZCand", xZCand, weight)

        weight = fakeEstimator.get_fake_weight(muons, -1)
        writer.fill_muons(
            f"3Mu/{region}/NonpromptDown/Incl/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/{region}/NonpromptDown/Incl/electrons", electrons, weight)
        writer.fill_jets(f"3Mu/{region}/NonpromptDown/Incl/jets", jets, weight)
        writer.fill_jets(
            f"3Mu/{region}/NonpromptDown/Incl/bjets", bjets, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptDown/Incl/METv", METv, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptDown/Incl/ZCand", ZCand, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptDown/Incl/xZCand", xZCand, weight)

        writer.fill_muons(
            f"3Mu/{region}/NonpromptDown/{measure}/muons", muons, weight)
        writer.fill_electrons(
            f"3Mu/{region}/NonpromptDown/{measure}/electrons", electrons, weight)
        writer.fill_jets(
            f"3Mu/{region}/NonpromptDown/{measure}/jets", jets, weight)
        writer.fill_jets(
            f"3Mu/{region}/NonpromptDown/{measure}/bjets", bjets, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptDown/{measure}/METv", METv, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptDown/{measure}/ZCand", ZCand, weight)
        writer.fill_object(
            f"3Mu/{region}/NonpromptDown/{measure}/xZCand", xZCand, weight)


def MCLoop(evt, writer, mcCorr, conv, syst):
    muon_momentum_shift = 0
    if syst == "MuonMomentumShiftUp":
        muon_momentum_shift = 1
    if syst == "MuonMomentumShiftDown":
        muon_momentum_shift = -1

    electron_energy_shift = 0
    electron_resolution_shift = 0

    muons = get_muons(evt, muon_momentum_shift)
    electrons = get_electrons(
        evt, electron_energy_shift, electron_resolution_shift)

    jet_energy_shift = 0
    if syst == "JetEnShiftUp":
        jet_energy_shift = 1
    if syst == "JetEnShiftDown":
        jet_energy_shift = -1
    jet_resolution_shift = 0
    if syst == "JetResShiftUp":
        jet_resolution_shift = 1
    if syst == "JetResShiftDown":
        jet_resolution_shift = -1

    jets, bjets = get_jets(evt, jet_energy_shift, jet_resolution_shift)
    METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)

    if not pass_baseline("3Mu", evt, muons, electrons, jets, bjets, "tight"):
        return None

    # prompt matching
    if not len(list(filter(lambda x: x.LepType() > 0, muons))) == 3:
        return None
    if not len(list(filter(lambda x: x.LepType() > 0, electrons))) == 0:
        return None

    if muons[0].Pt() < 20. or muons[1].Pt() < 20. or muons[2].Pt() < 20.:
        measure = "DYJets"
    else:
        measure = "ZGamma"

    sys_prefire = 0
    if syst == "L1PrefireUp":
        sys_prefire = 1
    if syst == "L1PrefireDown":
        sys_prefire = -1
    sys_pileup = 0
    if syst == "PileupCorrUp":
        sys_pileup = 1
    if syst == "PileupCorrDown":
        sys_pileup = -1
    sys_muon_idsf = 0
    if syst == "MuonIDSFUp":
        sys_muon_idsf = 1
    if syst == "MuonIDSFDown":
        sys_muon_idsf = -1
    sys_muon_trigsf = 0
    if syst == "DblMuonTrigSFUp":
        sys_muon_trigsf = 1
    if syst == "DblMuonTrigSFDown":
        sys_muon_trigsf = -1
    if args.scaleConv:
        sys_conv = 0
        if syst == "ConversionUp":
            sys_conv = 1
        if syst == "ConversionDown":
            sys_conv = -1

    weight = evt.GenWeight * evt.TrigLumi
    weight *= mcCorr.GetL1PrefireWeight(evt, sys_prefire)
    weight *= mcCorr.GetPileupWeight(evt.nPileUp, sys_pileup)
    weight *= mcCorr.GetMuonIDSF(muons, sys_muon_idsf)
    weight *= mcCorr.GetDblMuonTriggerSF(muons, sys_muon_trigsf)
    weight *= mcCorr.GetBtaggingWeight(jets)
    if args.scaleConv:
        if args.sample == "DYJets":
            weight *= conv.GetScale("DYJets", sys_conv)
        else:  # ZGmma
            weight *= conv.GetScale("ZGamma", sys_conv)

    writer.fill_muons(f"3Mu/Baseline/{syst}/Incl/muons", muons, weight)
    writer.fill_electrons(
        f"3Mu/Baseline/{syst}/Incl/electrons", electrons, weight)
    writer.fill_jets(f"3Mu/Baseline/{syst}/Incl/jets", jets, weight)
    writer.fill_jets(f"3Mu/Baseline/{syst}/Incl/bjets", bjets, weight)
    writer.fill_object(f"3Mu/Baseline/{syst}/Incl/METv", METv, weight)

    writer.fill_muons(f"3Mu/Baseline/{syst}/{measure}/muons", muons, weight)
    writer.fill_electrons(
        f"3Mu/Baseline/{syst}/{measure}/electrons", electrons, weight)
    writer.fill_jets(f"3Mu/Baseline/{syst}/{measure}/jets", jets, weight)
    writer.fill_jets(f"3Mu/Baseline/{syst}/{measure}/bjets", bjets, weight)
    writer.fill_object(f"3Mu/Baseline/{syst}/{measure}/METv", METv, weight)

    region = select("3Mu", evt, muons, electrons, jets, bjets, "tight")
    if not region:
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

    writer.fill_muons(f"3Mu/{region}/{syst}/Incl/muons", muons, weight)
    writer.fill_electrons(
        f"3Mu/{region}/{syst}/Incl/electrons", electrons, weight)
    writer.fill_jets(f"3Mu/{region}/{syst}/Incl/jets", jets, weight)
    writer.fill_jets(f"3Mu/{region}/{syst}/Incl/bjets", bjets, weight)
    writer.fill_object(f"3Mu/{region}/{syst}/Incl/METv", METv, weight)
    writer.fill_object(f"3Mu/{region}/{syst}/Incl/ZCand", ZCand, weight)
    writer.fill_object(f"3Mu/{region}/{syst}/Incl/xZCand", xZCand, weight)

    writer.fill_muons(f"3Mu/{region}/{syst}/{measure}/muons", muons, weight)
    writer.fill_electrons(
        f"3Mu/{region}/{syst}/{measure}/electrons", electrons, weight)
    writer.fill_jets(f"3Mu/{region}/{syst}/{measure}/jets", jets, weight)
    writer.fill_jets(f"3Mu/{region}/{syst}/{measure}/bjets", bjets, weight)
    writer.fill_object(f"3Mu/{region}/{syst}/{measure}/METv", METv, weight)
    writer.fill_object(f"3Mu/{region}/{syst}/{measure}/ZCand", ZCand, weight)
    writer.fill_object(f"3Mu/{region}/{syst}/{measure}/xZCand", xZCand, weight)


if __name__ == "__main__":
    if args.scaleConv:
        outfile_path = f"./output/ROOT/Skim3Mu__/withConv/{args.era}/{args.sample}.root"
    else:
        outfile_path = f"./output/ROOT/Skim3Mu__/{args.era}/{args.sample}.root"
    writer = HistogramWriter(
        outfile=outfile_path)
    if args.isData:
        fakeEstimator = FakeEstimator(era=args.era)
        f = TFile.Open(
            f"{os.environ['WORKDIR']}/SelectorOutput/{args.era}/Skim3Mu__/DATA/Selector_{args.sample}.root")
        for evt in f.Events:
            DataLoop(evt, writer, fakeEstimator)
    else:
        mcCorr = MCCorrection(era=args.era)
        mcCorr.SetBtaggingHandler(
            tagger="DeepJet", wp="Medium", syst="central")
        conv = Conversion(era=args.era)
        f = TFile.Open(
            f"{os.environ['WORKDIR']}/SelectorOutput/{args.era}/Skim3Mu__/Selector_{args.sample}.root")
        for evt in f.Events:
            for syst in Systematics:
                MCLoop(evt, writer, mcCorr, conv, syst)

    f.Close()
    writer.close()
