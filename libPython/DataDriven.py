from ROOT import TFile
import pandas as pd
import os
os.environ['WORKDIR'] = '/home/choij/workspace/ChargedHiggsAnalysis'


class FakeEstimator():
    def __init__(self, era):
        # set histogram for fake probability
        f = TFile.Open(
            f"{os.environ['WORKDIR']}/MetaInfo/{era}/fakerate_muon.root")
        h = f.Get("FR_cent_TopHNT_TopHNL")
        h.SetDirectory(0)
        f.Close()
        assert h
        self.h_fake = h

    def get_fake_probability(self, lepton, sys=0):
        ptCorr = lepton.Pt() * (1. + max(0., lepton.MiniIso() - 0.1))
        this_bin = self.h_fake.FindBin(ptCorr, abs(lepton.Eta()))
        fr = self.h_fake.GetBinContent(this_bin) * (1. + 0.3*sys)

        return fr

    def get_fake_weight(self, leptons, sys=0):
        out = -1.
        for lep in leptons:
            if lep.PassID("tight"):
                continue
            else:
                fr = self.get_fake_probability(lep, sys)
                out *= -1.*(fr / (1.-fr))

        return out


class Conversion():
    def __init__(self, era):
        csv_dyjets = pd.read_csv(
            f"{os.environ['WORKDIR']}/MetaInfo/{era}/Conversion/ScaleFactors_{era}_DYJets.csv", index_col="Sample")
        csv_zgamma = pd.read_csv(
            f"{os.environ['WORKDIR']}/MetaInfo/{era}/Conversion/ScaleFactors_{era}_ZGamma.csv", index_col="Sample")
        self.scale_dict = {
            "DYJets": (float(csv_dyjets.loc["Scale Factor", "Central"]), abs(float(csv_dyjets.loc["Scale Factor", "Total"].split(" ")[0]))),
            "ZGamma": (float(csv_zgamma.loc["Scale Factor", "Central"]), abs(float(csv_zgamma.loc["Scale Factor", "Total"].split(" ")[0])))
        }
        del csv_dyjets, csv_zgamma

    def GetScale(self, measure, sys=0):
        value, error = self.scale_dict[measure]
        return value + sys*error
