import os
import argparse
import ROOT
from array import array

wp_mvaNoIso = {
    "2016preVFP": {
        "EB1": 0.96,
        "EB2": 0.93,
        "EE": 0.85
    },
    "2016postVFP": {
        "EB1": 0.96,
        "EB2": 0.93,
        "EE": 0.85
    },
    "2017": {
        "EB1": 0.94,
        "EB2": 0.79,
        "EE": 0.50
    },
    "2018": {
        "EB1": 0.94,
        "EB2": 0.79,
        "EE": 0.50
    }
}

binning = array('d', [10., 15., 20., 25., 35., 50., 100., 200.])

class Electron:
    def __init__(self):
        self.pt = -999.
        self.scEta = -999.
        self.mvaNoIso = -999.
        self.miniRelIso = -999.
        self.sip3d = -999
        self.deltaR = -999.
        self.passMVANoIsoWP90 = False
        self.passMVANoIsoWPLoose = False
        self.nearestJetFlavour = -999
        self.genWeight = -999.
    
    def setPt(self, pt):
        self.pt = pt
    
    def setPtCorr(self):
        self.ptCorr = self.pt*(1.0 + max(0., self.miniRelIso-0.1))
        
    def setScEta(self, scEta):
        self.scEta = scEta
        
    def setMVANoIso(self, mvaNoIso):
        self.mvaNoIso = mvaNoIso
    
    def setMiniRelIso(self, miniRelIso):
        self.miniRelIso = miniRelIso
    
    def setSIP3D(self, sip3d):
        self.sip3d = sip3d
        
    def setDeltaR(self, deltaR):
        self.deltaR = deltaR
        
    def setID(self, passMVANoIsoWP90, passMVANoIsoWPLoose):
        self.passMVANoIsoWP90 = passMVANoIsoWP90
        self.passMVANoIsoWPLoose = passMVANoIsoWPLoose
        
    def setNearestJetFlavour(self, nearestJetFlavour):
        self.nearestJetFlavour = nearestJetFlavour
        
    # Only required HcToWA Veto ID while skimming
    def passLooseID(self, mvaNoIsoWP):
        if not (self.mvaNoIso > mvaNoIsoWP or self.passMVANoIsoWP90): return False
        if not self.miniRelIso < 0.6: return False
        if not self.sip3d < 6: return False
        return True
        
    def passTightID(self):
        if not self.passMVANoIsoWP90: return False
        if not self.miniRelIso < 0.1: return False
        if not self.sip3d < 4: return False
        return True


def parse_arguments():
    parser = argparse.ArgumentParser(description='Measure fake rate of electrons')
    parser.add_argument('--era', type=str, required=True, help='Era of data taking')
    parser.add_argument('--region', type=str, required=True, help="EB1, EB2, EE")
    parser.add_argument('--cut', type=float, default=-1, help="MVA cut" )
    args = parser.parse_args()
    return args

def is_valid_region(eta, region):
    if region == "EB1":
        return abs(eta) < 0.8
    elif region == "EB2":
        return abs(eta) > 0.8 and abs(eta) < 1.479
    elif region == "EE":
        return abs(eta) > 1.479 and abs(eta) < 2.5
    else:
        raise ValueError(f"Region {region} is not valid")    
    
def main():
    args = parse_arguments()
    loose_cut = wp_mvaNoIso[args.era][args.region] if args.cut < 0. else args.cut
    f = ROOT.TFile.Open(f"Skimmed/{args.era}/ElectronOptimization_TTLL_powheg.root")

    h_ljet_loose = ROOT.TH1F("ljet_loose", "", len(binning)-1, binning)
    h_cjet_loose = ROOT.TH1F("cjet_loose", "", len(binning)-1, binning)
    h_bjet_loose = ROOT.TH1F("bjet_loose", "", len(binning)-1, binning)

    h_ljet_tight = ROOT.TH1F("ljet_tight", "", len(binning)-1, binning)
    h_cjet_tight = ROOT.TH1F("cjet_tight", "", len(binning)-1, binning)
    h_bjet_tight = ROOT.TH1F("bjet_tight", "", len(binning)-1, binning)
    
    for evt in f.Events:
        electrons = []
        genWeight = evt.genWeight
        for i in range(evt.nElectrons):
            el = Electron()
            el.setPt(evt.Pt[i])
            el.setScEta(evt.scEta[i])
            el.setMVANoIso(evt.MVANoIso[i])
            el.setMiniRelIso(evt.MiniRelIso[i])
            el.setSIP3D(evt.SIP3D[i])
            el.setDeltaR(evt.DeltaR[i])
            el.setID(evt.PassMVANoIsoWP90[i], evt.PassMVANoIsoWPLoose[i])
            el.setNearestJetFlavour(evt.NearestJetFlavour[i])
            el.setPtCorr()
            electrons.append(el)
    
        for el in electrons:
            if el.deltaR > 0.4: continue
            if not is_valid_region(el.scEta, args.region): continue
            if not el.passLooseID(loose_cut): continue

            if el.nearestJetFlavour == 1:
                h_ljet_loose.Fill(el.ptCorr, genWeight)
                if el.passTightID(): h_ljet_tight.Fill(el.ptCorr, genWeight)
            elif el.nearestJetFlavour == 4:
                h_cjet_loose.Fill(el.ptCorr, genWeight)
                if el.passTightID(): h_cjet_tight.Fill(el.ptCorr, genWeight)
            elif el.nearestJetFlavour == 5:
                h_bjet_loose.Fill(el.ptCorr, genWeight)
                if el.passTightID(): h_bjet_tight.Fill(el.ptCorr, genWeight)
            else:
                continue 
    outpath = f"results/{args.era}/entries.{args.region}.{str(loose_cut).replace('.', 'p')}.root"
    os.makedirs(os.path.dirname(outpath), exist_ok=True) 
    out = ROOT.TFile(outpath, "RECREATE")
    out.cd()
    h_bjet_loose.Write()
    h_cjet_loose.Write()
    h_ljet_loose.Write()
    h_bjet_tight.Write()
    h_cjet_tight.Write()
    h_ljet_tight.Write()
    out.Close()
    
if __name__ == "__main__":
    main()
    
            
