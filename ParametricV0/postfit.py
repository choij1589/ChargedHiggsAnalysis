import ROOT
SIGNAL = "MHc-70_MA-65"
METHOD = "method2"


f = ROOT.TFile("higgsCombineTest.HybridNew.mH125.root")
w = f.Get("w")
w.Print("v")

n_bins = 80
binning = ROOT.RooFit.Binning(n_bins,45,85)

can = ROOT.TCanvas()
plot = w.var("mass").frame()
w.data("data_obs").plotOn( plot, binning )

# Load the S+B model
sb_model = w.pdf("model_s").getPdf("Tag0")

# Prefit
sb_model.plotOn( plot, ROOT.RooFit.LineColor(2), ROOT.RooFit.Name("prefit") )

# Postfit
w.loadSnapshot("HybridNew_mc_s__snapshot")
sb_model.plotOn( plot, ROOT.RooFit.LineColor(4), ROOT.RooFit.Name("postfit") )
r_bestfit = w.var("r").getVal()

# Bkg only
w.loadSnapshot("HybridNew_mc_b__snapshot")
sb_model.plotOn( plot, ROOT.RooFit.LineColor(6), ROOT.RooFit.Name("bkg only"))

plot.Draw()

leg = ROOT.TLegend(0.55,0.6,0.85,0.85)
leg.AddEntry("prefit", "Prefit S+B model (r=1.00)", "L")
leg.AddEntry("postfit", "Postfit S+B model (r=%.2f)"%r_bestfit, "L")
leg.AddEntry("bkg only", "Background only", "L")
leg.Draw("Same")

can.Update()
can.SaveAs(f"plots/{SIGNAL}/{METHOD}/postfit.png")
