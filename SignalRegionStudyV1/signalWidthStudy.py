import os
import ROOT as R
from ROOT import RooFit as RF
R.gROOT.SetBatch(True)

SIGNALs = ["MHc-70_MA-15",  "MHc-100_MA-15", "MHc-160_MA-15",
           "MHc-70_MA-40", "MHc-130_MA-55", "MHc-100_MA-60", "MHc-70_MA-65",
           "MHc-160_MA-85", "MHc-130_MA-90", "MHc-100_MA-95", "MHc-160_MA-120",
           "MHc-130_MA-125", "MHc-160_MA-155"]
ERA = "2016preVFP"
CHANNEL = "Skim3Mu"
WORKDIR = os.getenv("WORKDIR")

os.makedirs(f"plots/{ERA}/{CHANNEL}__", exist_ok=True)
os.makedirs(f"results/{ERA}/{CHANNEL}__", exist_ok=True)

#### find signal width by fitting MC with Double Crystall Ball function
def fitSignal(SIGNAL, mA):
    f_sig = R.TFile.Open(f"samples/{ERA}/{CHANNEL}__/{SIGNAL}/{SIGNAL}.root")
    tree = f_sig.Get(f"{SIGNAL}_Central")
    
    tempWidth = int(mA / 10.)
    mass = R.RooRealVar("mass", "mass", mA, mA-tempWidth, mA+tempWidth)
    weight = R.RooRealVar("weight", "weight", 0, -10, 10)
    mc_sig = R.RooDataSet("mc_sig", "mc_sig", tree, R.RooArgSet(mass, weight), "", "weight")
    
    ## fitting
    MA = R.RooRealVar("MA", "MA", mA, mA-tempWidth, mA+tempWidth)
    dMA = R.RooRealVar("dMA", "dMA", 0., -5., 5.)
    MA.setConstant(True)
    mean = R.RooFormulaVar("mean", "mean", "(@0+@1)", R.RooArgList(MA, dMA))
    
    sigma = R.RooRealVar("sigma", "sigma", mA/100, 0, 3)
    alphaL = R.RooRealVar("alphaL", "alphaL", -1, -10, 0);
    alphaR = R.RooRealVar("alphaR", "alphaR", 1, 0, 10);
    nL = R.RooRealVar("nL", "nL", 1, 0.1, 10)
    nR = R.RooRealVar("nR", "nR", 1, 0.1, 10)
    
    CBL = R.RooCBShape("CBL", "CBL", mass, mean, sigma, alphaL, nL)
    CBR = R.RooCBShape("CBR", "CBR", mass, mean, sigma, alphaR, nR)
    coeff = R.RooRealVar("coeff", "coeff", 0.5, 0., 1.)
    model = R.RooAddPdf("model_sig", "model_sig", R.RooArgList(CBL, CBR), R.RooArgList(coeff))
    model.fitTo(mc_sig, RF.SumW2Error(True), RF.PrintLevel(-1))
    
    ## print results
    print(MA, dMA)
    print(sigma)
    print(alphaL, alphaR)
    print(nL, nR)

    ## save plot
    can = R.TCanvas()
    plot = mass.frame()
    mc_sig.plotOn(plot)
    model.plotOn(plot, RF.LineColor(2))
    plot.Draw()
    can.Update()
    can.SaveAs(f"plots/{ERA}/{CHANNEL}__/{SIGNAL}.png")
    
    return {"MA": MA,
           "dMA": dMA,
           "sigma": sigma, 
           "alphaL": alphaL,
           "alphaR": alphaR,
           "nL": nL,
           "nR": nR}
    
def linearFit(path, savePath):
    # make a graph with csv file
    graph = R.TGraphErrors(path, format="%lg,%lg,%lg,%lg")

    graph.SetTitle("Measurement of #sigma_{A} [GeV]")
    graph.SetMarkerStyle(R.kOpenCircle)
    graph.SetMarkerColor(R.kBlue)
    graph.SetLineColor(R.kBlue)
    graph.GetXaxis().SetTitle("M_{A}")
    graph.GetYaxis().SetTitle("#sigma_{A}")
    graph.GetYaxis().SetRangeUser(0., 2.5)

    # define a linear function
    linear = R.TF1("linear function", "[0]+[1]*x", 0., 200.)
    linear.SetLineColor(R.kRed)
    linear.SetLineStyle(2)
    fitResult = graph.Fit(linear, option='S')
    chi2 = fitResult.Chi2() / fitResult.Ndf()
    with open(savePath, "a") as f:
        f.write(f"{linear.GetParameter(0)},{linear.GetParameter(1)},{chi2}\n")

    chi2String = R.TLatex()
    resultString = R.TLatex()
    can = R.TCanvas()
    graph.Draw("APE")
    linear.Draw("same")
    chi2String.DrawLatexNDC(0.15, 0.7, f"#chi^2/ndf = {chi2:.2f}")
    resultString.DrawLatexNDC(0.15, 0.6, f"{linear.GetParameter(0):.2e} + {linear.GetParameter(1):.2e}*x")
    can.SaveAs(f"plots/{ERA}/{CHANNEL}__/linearFitResult.png")
    
def quadraticFit(path, savePath):
    # make a graph with csv file
    graph = R.TGraphErrors(path, format="%lg,%lg,%lg,%lg")

    graph.SetTitle("Measurement of #sigma_{A} [GeV]")
    graph.SetMarkerStyle(R.kOpenCircle)
    graph.SetMarkerColor(R.kBlue)
    graph.SetLineColor(R.kBlue)
    graph.GetXaxis().SetTitle("M_{A}")
    graph.GetYaxis().SetTitle("#sigma_{A}")
    graph.GetYaxis().SetRangeUser(0., 2.5)

    # define a quadratic function
    quad = R.TF1("linear function", "[0]+[1]*x+[2]*x^2", 0., 200.)
    quad.SetLineColor(R.kRed)
    quad.SetLineStyle(2)
    fitResult = graph.Fit(quad, option='S')
    chi2 = fitResult.Chi2() / fitResult.Ndf()
    with open(savePath, "a") as f:
        f.write(f"{quad.GetParameter(0)},{quad.GetParameter(1)},{quad.GetParameter(2)},{chi2}\n")

    chi2String = R.TLatex()
    resultString = R.TLatex()
    can = R.TCanvas()
    graph.Draw("APE")
    quad.Draw("same")
    chi2String.DrawLatexNDC(0.15, 0.7, f"#chi^2/ndf = {chi2:.2f}")
    resultString.DrawLatexNDC(0.15, 0.6, f"{quad.GetParameter(0):.2e} + {quad.GetParameter(1):.2e}*x + {quad.GetParameter(2):.2e}*x^2")
    can.SaveAs(f"plots/{ERA}/{CHANNEL}__/quadFitResult.png")

def cubicFit(path, savePath):
    # make a graph with csv file
    graph = R.TGraphErrors(path, format="%lg,%lg,%lg,%lg")

    graph.SetTitle("Measurement of #sigma_{A} [GeV]")
    graph.SetMarkerStyle(R.kOpenCircle)
    graph.SetMarkerColor(R.kBlue)
    graph.SetLineColor(R.kBlue)
    graph.GetXaxis().SetTitle("M_{A}")
    graph.GetYaxis().SetTitle("#sigma_{A}")
    graph.GetYaxis().SetRangeUser(0., 2.5)

    # define a linear function
    cubic = R.TF1("linear function", "[0]+[1]*x+[2]*x^2+[3]*x^3", 0., 200.)
    cubic.SetLineColor(R.kRed)
    cubic.SetLineStyle(2)
    fitResult = graph.Fit(cubic, option='S')
    chi2 = fitResult.Chi2() / fitResult.Ndf()
    with open(savePath, "a") as f:
        f.write(f"{cubic.GetParameter(0)},{cubic.GetParameter(1)},{cubic.GetParameter(2)},{cubic.GetParameter(3)},{chi2}\n")

    chi2String = R.TLatex()
    resultString = R.TLatex()
    can = R.TCanvas()
    graph.Draw("APE")
    cubic.Draw("same")
    chi2String.DrawLatexNDC(0.15, 0.7, f"#chi^2/ndf = {chi2:.2f}")
    resultString.DrawLatexNDC(0.15, 0.6, f"{cubic.GetParameter(0):.2e} + {cubic.GetParameter(1):.2e}*x + {cubic.GetParameter(2):.2e}*x^2 + {cubic.GetParameter(3):.2f}*x^3")
    can.SaveAs(f"plots/{ERA}/{CHANNEL}__/cubicFitResult.png")
    
if __name__ == "__main__":
    # make a csv file to make a graph
    filePath = f"results/{ERA}/{CHANNEL}__/AmassFitResults.csv"
    savePath = f"results/{ERA}/{CHANNEL}__/interpolResults.csv"
    with open(savePath, "w") as f:
        f.write("#parameters,chi2\n")
    f = open(filePath, "w")
    for SIGNAL in SIGNALs:
        mA = int(SIGNAL.split("_")[1].split("-")[1])
        results = fitSignal(SIGNAL, mA)
        f.write(f"{mA},{results['sigma'].getValV()},0,{results['sigma'].getError()}\n")
    f.close()
    
    linearFit(filePath, savePath)
    quadraticFit(filePath, savePath)
    cubicFit(filePath, savePath)
