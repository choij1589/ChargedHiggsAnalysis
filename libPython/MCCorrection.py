from argparse import ArgumentError
import os
import pandas as pd
from math import log
from ROOT import TFile

class MCCorrection():
    def __init__(self, era):
        self.era = era
        
        # get histograms
        # pileup
        f = TFile.Open(f"{os.environ['WORKDIR']}/MetaInfo/{era}/pileUp.root")
        h_pileup_central = f.Get(f"MC_{era}_central"); h_pileup_central.SetDirectory(0)
        h_pileup_systup = f.Get(f"MC_{era}_sig_up"); h_pileup_systup.SetDirectory(0)
        h_pileup_systdown = f.Get(f"MC_{era}_sig_down"); h_pileup_systdown.SetDirectory(0)
        f.Close()
        assert h_pileup_central and h_pileup_systup and h_pileup_systdown
        self.h_pileup_central = h_pileup_central
        self.h_pileup_systup = h_pileup_systup
        self.h_pileup_systdown = h_pileup_systdown
        
        # ID, trigger
        f = TFile.Open(f"{os.environ['WORKDIR']}/MetaInfo/{era}/efficiency_TopHN_IDIso.root")
        h_muon_idsf = f.Get("SF_fabs(probe_eta)_probe_pt"); h_muon_idsf.SetDirectory(0)
        f.Close()
        assert h_muon_idsf
        self.h_muon_idsf = h_muon_idsf
        
        f = TFile.Open(f"{os.environ['WORKDIR']}/MetaInfo/{era}/efficiency_Mu17Leg1_DoubleMuonTriggers.root")
        h_dblmu_trig_eff_leg1_data = f.Get("muonEffi_data_fabs(probe_eta)_probe_pt"); h_dblmu_trig_eff_leg1_data.SetDirectory(0)
        h_dblmu_trig_eff_leg1_mc = f.Get("muonEffi_mc_fabs(probe_eta)_probe_pt"); h_dblmu_trig_eff_leg1_mc.SetDirectory(0)
        f.Close()
        assert h_dblmu_trig_eff_leg1_data and h_dblmu_trig_eff_leg1_mc
        self.h_dblmu_trig_eff_leg1_data = h_dblmu_trig_eff_leg1_data
        self.h_dblmu_trig_eff_leg1_mc = h_dblmu_trig_eff_leg1_mc
        
        f = TFile.Open(f"{os.environ['WORKDIR']}/MetaInfo/{era}/efficiency_Mu8Leg2_DoubleMuonTriggers.root")
        h_dblmu_trig_eff_leg2_data = f.Get("muonEffi_data_fabs(probe_eta)_probe_pt"); h_dblmu_trig_eff_leg2_data.SetDirectory(0)
        h_dblmu_trig_eff_leg2_mc = f.Get("muonEffi_mc_fabs(probe_eta)_probe_pt"); h_dblmu_trig_eff_leg2_mc.SetDirectory(0)
        f.Close()
        assert h_dblmu_trig_eff_leg2_data and h_dblmu_trig_eff_leg2_mc
        self.h_dblmu_trig_eff_leg2_data = h_dblmu_trig_eff_leg2_data
        self.h_dblmu_trig_eff_leg2_mc = h_dblmu_trig_eff_leg2_mc
        
    def SetBtaggingHandler(self, tagger, wp, syst="central"):
        if not tagger in ["DeepCSV", "DeepJet"]:
            print(f"[MCCorrection::SetBtaggingHandler] Wrong tagger {tagger}")
            raise(ArgumentError)
        if not wp in ["Loose", "Medium", "Tight"]:
            print(f"[MCCorrection::SetBtaggingHandler] Wrong wp {wp}")
            raise(ArgumentError)
        
        # Get MC tagging effciencies
        f = TFile.Open(f"{os.environ['WORKDIR']}/MetaInfo/{self.era}/BTag/MeasureJetTaggingEfficiency_TTLL_TTLJ_hadded.root")
        j_eff_B_denom = f.Get(f"Jet_{self.era}_eff_B_denom"); j_eff_B_denom.SetDirectory(0)
        j_eff_C_denom = f.Get(f"Jet_{self.era}_eff_C_denom"); j_eff_C_denom.SetDirectory(0)
        j_eff_L_denom = f.Get(f"Jet_{self.era}_eff_Light_denom"); j_eff_L_denom.SetDirectory(0)
        
        j_eff_B_num = f.Get(f"Jet_{self.era}_{tagger}_{wp}_eff_B_num"); j_eff_B_num.SetDirectory(0)
        j_eff_C_num = f.Get(f"Jet_{self.era}_{tagger}_{wp}_eff_C_num"); j_eff_C_num.SetDirectory(0)
        j_eff_L_num = f.Get(f"Jet_{self.era}_{tagger}_{wp}_eff_Light_num"); j_eff_L_num.SetDirectory(0)
        f.Close()
        
        self.JetBTaggingMCEffB = j_eff_B_num.Clone("j_eff_B"); self.JetBTaggingMCEffB.Divide(j_eff_B_denom)
        self.JetBTaggingMCEffC = j_eff_C_num.Clone("j_eff_C"); self.JetBTaggingMCEffC.Divide(j_eff_C_denom)
        self.JetBTaggingMCEffL = j_eff_L_num.Clone("j_eff_L"); self.JetBTaggingMCEffL.Divide(j_eff_L_denom)
        
        formula = "formula" if self.era in ["2016preVFP", "2016postVFP"] else "formula "
        if self.era in ["2016postVFP", "2017"]:
            JetSF = pd.read_csv(
                        f"{os.environ['WORKDIR']}/MetaInfo/{self.era}/BTag/wp_{tagger[0].lower()+tagger[1:]}_106XUL{self.era[2:]}_v3.csv")
        else:
            JetSF = pd.read_csv(
                        f"{os.environ['WORKDIR']}/MetaInfo/{self.era}/BTag/wp_{tagger[0].lower()+tagger[1:]}_106XUL{self.era[2:]}_v2.csv")
        
        JetSFH = JetSF.loc[(JetSF['OperatingPoint'] == wp[0]) &
                           (JetSF['measurementType'] == 'mujets') &
                           (JetSF['sysType'] == syst)]
        JetSFL = JetSF.loc[(JetSF['OperatingPoint'] == wp[0]) &
                           (JetSF['measurementType'] == 'incl') &
                           (JetSF['sysType'] == syst)]
        self.JetBTaggingSFB = JetSFH.loc[JetSF['jetFlavor'] == 5, formula].values[0]
        self.JetBTaggingSFC = JetSFH.loc[JetSF['jetFlavor'] == 4, formula].values[0]
        self.JetBTaggingSFL = JetSFL.loc[JetSF['jetFlavor'] == 0, formula].values[0]
    
    def GetL1PrefireWeight(self, evt, sys=0):
        if sys == 0:
            return evt.L1PrefireWeight
        elif sys == +1:
            return evt.L1PrefireWeightUp
        elif sys == -1:
            return evt.L1PrefireWeightDown
        else:
            print(f"[MCCorrection::getL1PrefireWeight] Wrong sys {sys}")
            raise(ArgumentError)
        
    def GetPileupWeight(self, nPileUp, sys=0):
        this_bin = self.h_pileup_central.FindBin(nPileUp)
        if sys == 0:
            return self.h_pileup_central.GetBinContent(this_bin)
        elif sys == +1:
            return self.h_pileup_systup.GetBinContent(this_bin)
        elif sys == -1:
            return self.h_pileup_systdown.GetBinContent(this_bin)
        else:
            print(f"[MCCorrection::getPileUpWeight] Wrong sys {sys}")
            raise(ArgumentError)
    
    def __GetMuonIDSF(self, muon, sys=0):
        pt = min( max(10., muon.Pt()), 199.)
        eta = min( abs(muon.Eta()), 2.39)
        this_bin = self.h_muon_idsf.FindBin(eta, pt)
        value = self.h_muon_idsf.GetBinContent(this_bin)
        error = self.h_muon_idsf.GetBinError(this_bin)
        
        return value + sys*error

    def GetMuonIDSF(self, muons, sys=0):
        sf = 1.
        for mu in muons:
            sf *= self.__GetMuonIDSF(mu, sys)
        return sf
    
    def __GetDblMuonTriggerEff(self, muon, leg, is_data, sys=0):
        if not leg in ["Mu17Leg1", "Mu8Leg2"]:
            print(f"[MCCorrection::__GetDblMuonTriggerEff] Wrong leg {leg}")
            raise(ArgumentError)
        
        if leg == "Mu17Leg1":
            if is_data: this_hist = self.h_dblmu_trig_eff_leg1_data
            else:       this_hist = self.h_dblmu_trig_eff_leg1_mc
        else:
            if is_data: this_hist = self.h_dblmu_trig_eff_leg2_data
            else:       this_hist = self.h_dblmu_trig_eff_leg2_mc
        
        pt = min( max(10., muon.Pt()), 199.)
        eta = min( abs(muon.Eta()), 2.39)
        this_bin = this_hist.FindBin(eta, pt)
        value, error = this_hist.GetBinContent(this_bin), this_hist.GetBinError(this_bin)
        
        return value + sys*error
    
    def GetDblMuonTriggerEff(self, muons, is_data, sys=0):
        eff = 1.
        
        # dz filter eff
        eff_dz = 1.
        if self.era == "2016postVFP":
            eff_dz = 0.9798 if is_data else 0.9969
        elif self.era == "2017":
            eff_dz = 0.9958
        else:
            pass
        
        if len(muons) == 2:
            eff *= self.__GetDblMuonTriggerEff(muons[0], "Mu17Leg1", is_data, sys)
            eff *= self.__GetDblMuonTriggerEff(muons[1], "Mu8Leg2", is_data, sys)
            eff *= eff_dz
        elif len(muons) == 3:
            eff1, eff2, eff3 = 1., 1., 1.
            # Case 1. mu1 fire leg1 and mu2 fire leg2
            eff1 *= self.__GetDblMuonTriggerEff(muons[0], "Mu17Leg1", is_data, sys)
            eff1 *= self.__GetDblMuonTriggerEff(muons[1], "Mu8Leg2", is_data, sys)
            eff1 *= eff_dz
            # Case 2. mu1 fire leg1 and mu3 fire leg2
            eff2 *= self.__GetDblMuonTriggerEff(muons[0], "Mu17Leg1", is_data, sys)
            eff2 *= (1. - self.__GetDblMuonTriggerEff(muons[1], "Mu8Leg2", is_data, sys)*eff_dz)
            eff2 *= self.__GetDblMuonTriggerEff(muons[2], "Mu8Leg2", is_data, sys)
            eff2 *= eff_dz
            # Case 3. mu2 fire leg1 and mu3 fire leg2
            eff3 *= (1. - self.__GetDblMuonTriggerEff(muons[0], "Mu17Leg1", is_data, sys)*eff_dz)
            eff3 *= self.__GetDblMuonTriggerEff(muons[1], "Mu17Leg1", is_data, sys)
            eff3 *= self.__GetDblMuonTriggerEff(muons[2], "Mu8Leg2", is_data, sys)
            eff3 *= eff_dz
            eff = eff1+eff2+eff3
        else:
            print(f"[MCCorrection::GetDblMuonTriggerEff] Wrong number of muons {len(muons)}")
            raise(ValueError)
        
        return eff

    def GetDblMuonTriggerSF(self, muons, sys=0):
        trigeff_data = self.GetDblMuonTriggerEff(muons, True, sys)
        trigeff_mc = self.GetDblMuonTriggerEff(muons, False, sys)
        if trigeff_mc == 0.:
            return 1.
        
        return trigeff_data / trigeff_mc
    
    def __GetMCJetTaggingEff(self, jet, sys=0):
        pt = min(1000., max(20., jet.Pt()))
        eta = min(2.5, max(-2.5, jet.Eta()))

        if jet.HadronFlavour() == 0:
            this_hist = self.JetBTaggingMCEffL
        elif jet.HadronFlavour() == 4:
            this_hist = self.JetBTaggingMCEffC
        elif jet.HadronFlavour() == 5:
            this_hist = self.JetBTaggingMCEffB
        else:
            print("[MCCorrection::__GetMCJetTaggingEff] wrong hadron flavour, this should not be happen")
            exit(1)
        this_bin = this_hist.FindBin(abs(eta), pt)
        value, error = this_hist.GetBinContent(this_bin), this_hist.GetBinError(this_bin)
        out = value+sys*error
        return out
    
    def __GetJetTaggingSF(self, jet, sys=0):
        if jet.HadronFlavour() == 0:
            formula = self.JetBTaggingSFL
        elif jet.HadronFlavour() == 4:
            formula = self.JetBTaggingSFC
        elif jet.HadronFlavour() == 5:
            formula = self.JetBTaggingSFB
        else:
            pass
        
        x = min(max(0., jet.Pt()), 1000.)
        sf = eval(formula)
            
        return sf
    
    def GetBtaggingWeight(self, jets):
        prob_data = 1.
        prob_mc = 1.
        for jet in jets:
            this_mc_eff = self.__GetMCJetTaggingEff(jet)
            this_data_eff = this_mc_eff*self.__GetJetTaggingSF(jet)

            if jet.IsBtagged():
                prob_data *= this_data_eff
                prob_mc *= this_mc_eff
            else:
                prob_data *= (1. - this_data_eff)
                prob_mc *= (1. - this_mc_eff)
        
        if prob_data > 0. and prob_mc > 0.:
            return prob_mc / prob_data
        else:
            return 1.
            
