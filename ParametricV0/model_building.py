import ROOT as R
from ROOT import RooFit as RF
R.gROOT.SetBatch(True)

SIGNAL = "MHc-70_MA-65"
ERA = "2018"
CHANNEL = "Skim3Mu"
NETWORK = "DenseNet"
METHOD = "method2"

#### Signal Modelling
f_sig = R.TFile(f"{SIGNAL}/{ERA}/{CHANNEL}__{NETWORK}__/{METHOD}/{SIGNAL}.root")
tree = f_sig.Get("Events")

mass = R.RooRealVar("mass", "mass", 65, 55, 75)
weight = R.RooRealVar("weight", "weight", 0, -10, 10)

mc_sig = R.RooDataSet("mc_sig", "mc_sig", tree, R.RooArgSet(mass, weight), "", "weight")

# fitting
MA = R.RooRealVar("MA", "MA", 65, 60, 70)
dMA = R.RooRealVar("dMA", "dMA", 0., -5., 5.)
MA.setConstant(True)
mean = R.RooFormulaVar("mean", "mean", "(@0+@1)", R.RooArgList(MA, dMA))

sigma = R.RooRealVar("sigma", "sigma", 2, 0, 5)
alphaL = R.RooRealVar("alphaL", "alphaL", -1, -10, 0);
alphaR = R.RooRealVar("alphaR", "alphaR", 1, 0, 10);
nL = R.RooRealVar("nL", "nL", 1, 0.1, 10)
nR = R.RooRealVar("nR", "nR", 1, 0.1, 10)

CBL = R.RooCBShape("CBL", "CBL", mass, mean, sigma, alphaL, nL)
CBR = R.RooCBShape("CBR", "CBR", mass, mean, sigma, alphaR, nR)
coeff = R.RooRealVar("coeff", "coeff", 0.5, 0., 1.)
model = R.RooAddPdf("model_sig", "model_sig", R.RooArgList(CBL, CBR), R.RooArgList(coeff))
model.fitTo(mc_sig, RF.SumW2Error(True), RF.PrintLevel(-1))
print(mc_sig.sumEntries())

# save results
dMA.setConstant(True)
sigma.setConstant(True)
alphaL.setConstant(True)
alphaR.setConstant(True)
nL.setConstant(True)
nR.setConstant(True)
coeff.setConstant(True)

f_out = R.TFile("workspace_sig.root", "recreate")
w_sig = R.RooWorkspace("workspace_sig", "workspace_sig")
getattr(w_sig, "import")(model)
w_sig.Print()
w_sig.Write()
f_sig.Close()
f_out.Close()

can = R.TCanvas()
plot = mass.frame()
mc_sig.plotOn(plot)
model.plotOn(plot, RF.LineColor(2))
plot.Draw()
can.Update()
can.SaveAs(f"plots/{SIGNAL}/{METHOD}/signal_model.png")

#### Background modelling
f_bkg = R.TFile(f"{SIGNAL}/{ERA}/{CHANNEL}__{NETWORK}__/{METHOD}/Background.root")
tree = f_bkg.Get("Events")

mc_bkg = R.RooDataSet("mc_bkg", "mc_bkg", tree, R.RooArgSet(mass, weight), "", "weight");

# fitting
alpha = R.RooRealVar("alpha", "alpha", -0.05, -0.2, 0.)
model_bkg = R.RooExponential("model_bkg", "model_bkg", mass, alpha)
model_bkg.fitTo(mc_bkg, RF.SumW2Error(True), RF.PrintLevel(-1))

norm = R.RooRealVar("model_bkg_norm", "no. of background events in SR", mc_bkg.sumEntries(), 0.8*mc_bkg.sumEntries(), 1.2*mc_bkg.sumEntries())
alpha.setConstant(False)

f_out = R.TFile("workspace_bkg.root", "recreate")
w_bkg = R.RooWorkspace("workspace_bkg", "workspace_bkg")
getattr(w_bkg, "import")(mc_bkg)
getattr(w_bkg, "import")(norm)
getattr(w_bkg, "import")(model_bkg)
w_bkg.Print()
w_bkg.Write()
f_bkg.Close()
f_out.Close()

can = R.TCanvas()
plot = mass.frame()
mc_bkg.plotOn(plot)
model_bkg.plotOn(plot, RF.LineColor(2))
plot.Draw()
can.Update()
can.Draw()
can.SaveAs(f"plots/{SIGNAL}/{METHOD}/background_model.png")
