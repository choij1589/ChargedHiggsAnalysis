import os
import argparse
import ROOT

def parse_arguments():
    parser = argparse.ArgumentParser(description='Measure fake rate of electrons')
    parser.add_argument('--era', type=str, required=True, help='Era of data taking')
    parser.add_argument('--region', type=str, required=True, help="EB1, EB2, EE")
    #parser.add_argument('--cut', type=float, required=True, help="MVA Cut Value for loose ID")
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
    h_MVANoIsoWPLoose = ROOT.TH2F("h_MVANoIsoWPLoose_ptCorr_vs_mva", "MVANoIsoWPLoose_ptCorr_vs_mva", 40, 0, 200, 180, -0.8, 1.)
    h_MVANoIsoWP90 = ROOT.TH2F("h_MVANoIsoWP90_ptCorr_vs_mva", "MVANoIsoWP90_ptCorr_vs_mva", 40, 0, 200, 180, -0.8, 1.)
    h_MVANoIsoWPLoose.SetDirectory(0)
    h_MVANoIsoWP90.SetDirectory(0)
    
    for evt in f.Events:
        for i in range(evt.nElectrons):
            if not is_valid_region(evt.scEta[i], args.region): continue
            ptCorr = evt.ptCorr[i]
            mva    = evt.MVANoIso[i]
            
            if not evt.PassMVANoIsoWPLoose[i]: continue
            h_MVANoIsoWPLoose.Fill(ptCorr, mva)
            
            if not evt.PassMVANoIsoWP90[i]: continue
            h_MVANoIsoWP90.Fill(ptCorr, mva)
    f.Close()
    
    # save histograms
    outpath = f"results/{args.era}/CheckTightMVACut_{args.region}.root"
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    out = ROOT.TFile(outpath, "RECREATE")
    out.cd()
    h_MVANoIsoWPLoose.Write()
    h_MVANoIsoWP90.Write()
    out.Close()
    
if __name__ == "__main__":
    main()
    
        
    