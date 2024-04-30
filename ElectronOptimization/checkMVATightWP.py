import os
import argparse
import ROOT

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
        if not self.mvaNoIso > mvaNoIsoWP: return False
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
    f = ROOT.TFile.Open(f"Skimmed/{args.era}/ElectronOptimization_TTLL_powheg.root")
    h_veto = ROOT.TH2F("pT_vs_mvaNoIso_passVeto", "", 28, 10, 150, 200, -1, 1)
    h_tight = ROOT.TH2F("pT_vs_mvaNoIso_passTight", "", 28, 10, 150, 200, -1, 1)
    
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
            if not is_valid_region(el.scEta, args.region): continue

            h_veto.Fill(el.pt, el.mvaNoIso, genWeight)
            if not el.passMVANoIsoWP90: continue
            if not el.miniRelIso < 0.1: continue
            if not el.sip3d < 4: continue
            h_tight.Fill(el.pt, el.mvaNoIso, genWeight)

    outpath = f"results/{args.era}/mvaNoIso_{args.region}.root"
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    out = ROOT.TFile(outpath, "RECREATE")
    out.cd()
    h_veto.Write()
    h_tight.Write()
    out.Close()

if __name__ == "__main__":
    main()
