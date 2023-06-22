import argparse
import ROOT

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--method", required=True, type=str, help="method")
args = parser.parse_args()

lumiString = {
    "2016preVFP": "L_{int} = 19.5 fb^{-1}",
    "2016postVFP": "L_{int} = 16.8 fb^{-1}",
    "2017": "L_{int} = 41.5 fb^{-1}",
    "2018": "L_{int} = 59.8 fb^{-1}"
}

def drawTemplate(signal):
    # get root file
    rtpath = f"results/{args.era}/{args.channel}__{args.method}__/{signal}/shapes_input.root"
    f = ROOT.TFile(rtpath, "read")
    
    sig = f.Get(signal)
    bkg = f.Get("data_obs")
    
    sig.SetStats(0)
    sig.SetLineColor(ROOT.kBlack)
    sig.SetLineWidth(2)
    sig.GetXaxis().SetTitle("M(#mu^{+}#mu^{-})")
    sig.GetYaxis().SetTitle("N_{pairs}")
    
    bkg.SetStats(0)
    bkg.SetLineColor(ROOT.kRed)
    bkg.SetLineWidth(2)
    bkg.GetXaxis().SetTitle("M(#mu^{+}#mu^{-})")
    bkg.GetYaxis().SetTitle("N_{pairs}")
    
    if sig.GetMaximum() > bkg.GetMaximum():
        sig.GetYaxis().SetRangeUser(0., sig.GetMaximum()*1.6)
        bkg.GetYaxis().SetRangeUser(0., sig.GetMaximum()*1.6)
    else:
        sig.GetYaxis().SetRangeUser(0., bkg.GetMaximum()*1.6)
        bkg.GetYaxis().SetRangeUser(0., bkg.GetMaximum()*1.6)
    
    lg = ROOT.TLegend(0.65, 0.65, 0.87, 0.85)
    lg.SetFillStyle(0)
    lg.SetBorderSize(0)
    lg.AddEntry(sig, "exp. sig.", "l")
    lg.AddEntry(bkg, "exp. bkg.", "lep")
    
    text = ROOT.TLatex()
    
    c = ROOT.TCanvas("c", "", 800, 800)
    c.cd()
    bkg.Draw()
    sig.Draw("hist&same")
    
    text.SetTextSize(0.04)
    text.SetTextFont(61)
    text.DrawLatexNDC(0.17, 0.83, "CMS")
    
    text.SetTextSize(0.035)
    text.SetTextFont(52)
    text.DrawLatexNDC(0.17, 0.78, "Work in progress") 
    
    text.SetTextSize(0.035)
    text.SetTextFont(42)
    text.DrawLatexNDC(0.7, 0.912, lumiString[args.era])
    
    c.SaveAs(f"plots/template.{args.era}.{args.channel}.{args.method}.{signal}.png")
    f.Close()
    c.Close()
    
if __name__ == "__main__":
    signals = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
               "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
               "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
               "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
    if args.method == "GNNOptim":
        signals = ["MHc-70_MA-65", "MHc-100_MA-95", "MHc-130_MA-90", "MHc-160_MA-85", "MHc-160_MA-120"]
    
    for signal in signals:
        drawTemplate(signal)
    
    
