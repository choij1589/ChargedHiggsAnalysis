# %%
import os
import ROOT

# %%
## Environment settings
WORKDIR = "/home/choij/workspace/ChargedHiggsAnalysis"
ERA = "2018"
CHANNEL = "Skim3Mu"

SIGNALs = ["TTToHcToWAToMuMu_MHc-70_MA-15",
           "TTToHcToWAToMuMu_MHc-70_MA-40",
           "TTToHcToWAToMuMu_MHc-70_MA-65",
           "TTToHcToWAToMuMu_MHc-100_MA-15",
           "TTToHcToWAToMuMu_MHc-100_MA-60",
           "TTToHcToWAToMuMu_MHc-100_MA-95",
           "TTToHcToWAToMuMu_MHc-130_MA-15",
           "TTToHcToWAToMuMu_MHc-130_MA-55",
           "TTToHcToWAToMuMu_MHc-130_MA-90",
           "TTToHcToWAToMuMu_MHc-130_MA-125",
           "TTToHcToWAToMuMu_MHc-160_MA-15",
           "TTToHcToWAToMuMu_MHc-160_MA-85",
           "TTToHcToWAToMuMu_MHc-160_MA-120",
           "TTToHcToWAToMuMu_MHc-160_MA-155"]
NONPROMPTs = ["DYJets", "DYJets_MG", "DYJets10to50_MG", "TTLL_powheg"]
BACKGROUNDs = ["DYJets", "ZGToLLG",                       # Nonprompt / Conversion
               "ttWToLNu", "ttZToLLNuNu", "ttHToNonbb",   # tt+X
               "WZTo3LNu_amcatnlo", "ZZTo4L_powheg",      # VV
               "WWW", "WWZ", "WZZ", "ZZZ",                # VVV
               "GluGluHToZZTo4L", "VBF_HToZZTo4L",        # H to ZZ to 4L
               "tHq", "TTG", "tZq"]                       # rare processes
SAMPLEs = SIGNALs + BACKGROUNDs

os.makedirs(f"plots/{ERA}/{CHANNEL}__")
os.makedirs(f"plots/{ERA}/{CHANNEL}__FakeStudy__")

# %%
for SAMPLE in NONPROMPTs:
    f = ROOT.TFile.Open(f"{WORKDIR}/data/AcceptanceStudy/{ERA}/{CHANNEL}__FakeStudy__/AcceptanceStudy_{SAMPLE}.root")
    cutflow = f.Get("cutflow")
    nTotal = cutflow.GetBinContent(1)
    nFinal = cutflow.GetBinContent(10)
    print(f"{SAMPLE}\t{nFinal}\t{nTotal}\t{nFinal/nTotal}")
    f.Close()

for SAMPLE in SAMPLEs:
    f = ROOT.TFile.Open(f"{WORKDIR}/data/AcceptanceStudy/{ERA}/{CHANNEL}__/AcceptanceStudy_{SAMPLE}.root")
    cutflow = f.Get("cutflow")
    nTotal = cutflow.GetBinContent(1)
    nFinal = cutflow.GetBinContent(10)
    print(f"{SAMPLE}\t{nFinal}\t{nTotal}\t{nFinal/nTotal}")
    f.Close()

for SAMPLE in NONPROMPTs:
    f = ROOT.TFile.Open(f"{WORKDIR}/data/AcceptanceStudy/{ERA}/{CHANNEL}__FakeStudy__/AcceptanceStudy_{SAMPLE}.root")
    cutflow = f.Get("cutflow")
    cutflow.SetStats(0)
    cutflow.SetLineColor(ROOT.kBlack)
    cutflow.SetFillColorAlpha(ROOT.kRed, 0.5)
    cutflow.SetLineWidth(2)
    cutflow.SetTitle(f"cutflow for {SAMPLE}")

    nTotal = cutflow.GetBinContent(1)
    nFinal = cutflow.GetBinContent(10)
    for bin in range(1, cutflow.GetNbinsX()+1):
        cutflow.SetBinContent(bin, cutflow.GetBinContent(bin) / nTotal)

    cutflow.GetXaxis().SetTitle("cuts"); cutflow.GetXaxis().SetTitleOffset(0.7)
    cutflow.GetYaxis().SetTitle("efficiency"); cutflow.GetYaxis().SetTitleOffset(0.7)
    cutflow.GetYaxis().SetRangeUser(cutflow.GetBinContent(10) / 5, 8)
    cutflow.GetXaxis().SetBinLabel(1, 'total')
    cutflow.GetXaxis().SetBinLabel(2, 'MET filter')
    cutflow.GetXaxis().SetBinLabel(3, 'lepton no.')
    cutflow.GetXaxis().SetBinLabel(4, 'prompt matching')
    cutflow.GetXaxis().SetBinLabel(5, 'trigger')
    cutflow.GetXaxis().SetBinLabel(6, 'OS charged')
    cutflow.GetXaxis().SetBinLabel(7, 'mass > 12 GeV')
    cutflow.GetXaxis().SetBinLabel(8, 'N_{j} \ge 2')
    cutflow.GetXaxis().SetBinLabel(9, 'N_{b} \ge 1')
    cutflow.GetXaxis().SetBinLabel(10, '60 < mass < 120 GeV')

    eff = ROOT.TLatex(); eff.SetTextSize(0.03)
    initEvt = ROOT.TLatex(); initEvt.SetTextSize(0.03)
    finalEvt = ROOT.TLatex(); finalEvt.SetTextSize(0.03)

    c = ROOT.TCanvas("canvas", "", 800, 800)
    c.cd()
    c.SetLogy()
    cutflow.Draw("hist&text30")
    initEvt.DrawLatexNDC(0.55, 0.8, f"initial Evts = {nTotal:.6f}")
    finalEvt.DrawLatexNDC(0.55, 0.75, f"final Evts = {nFinal:.6f}")
    eff.DrawLatexNDC(0.55, 0.7, f"efficiency = {nFinal / nTotal * 100:.4f}%")

    c.RedrawAxis()
    c.SaveAs(f"plots/{ERA}/{CHANNEL}__FakeStudy__/cutflow_{SAMPLE}.png")
    f.Close()


for SAMPLE in SAMPLEs:
    f = ROOT.TFile.Open(f"{WORKDIR}/data/AcceptanceStudy/{ERA}/{CHANNEL}__/AcceptanceStudy_{SAMPLE}.root")
    cutflow = f.Get("cutflow")
    cutflow.SetStats(0)
    cutflow.SetLineColor(ROOT.kBlack)
    cutflow.SetFillColorAlpha(ROOT.kGreen, 0.5)
    cutflow.SetLineWidth(2)
    cutflow.SetTitle(f"cutflow for {SAMPLE}")

    nTotal = cutflow.GetBinContent(1)
    nFinal = cutflow.GetBinContent(10)
    for bin in range(1, cutflow.GetNbinsX()+1):
        cutflow.SetBinContent(bin, cutflow.GetBinContent(bin) / nTotal)

    cutflow.GetXaxis().SetTitle("cuts"); cutflow.GetXaxis().SetTitleOffset(0.7)
    cutflow.GetYaxis().SetTitle("efficiency"); cutflow.GetYaxis().SetTitleOffset(0.7)
    cutflow.GetYaxis().SetRangeUser(cutflow.GetBinContent(10) / 5, 8)
    cutflow.GetXaxis().SetBinLabel(1, 'total')
    cutflow.GetXaxis().SetBinLabel(2, 'MET filter')
    cutflow.GetXaxis().SetBinLabel(3, 'lepton no.')
    cutflow.GetXaxis().SetBinLabel(4, 'prompt matching')
    cutflow.GetXaxis().SetBinLabel(5, 'trigger')
    cutflow.GetXaxis().SetBinLabel(6, 'OS charged')
    cutflow.GetXaxis().SetBinLabel(7, 'mass > 12 GeV')
    cutflow.GetXaxis().SetBinLabel(8, 'N_{j} \ge 2')
    cutflow.GetXaxis().SetBinLabel(9, 'N_{b} \ge 1')
    cutflow.GetXaxis().SetBinLabel(10, '60 < mass < 120 GeV')

    eff = ROOT.TLatex(); eff.SetTextSize(0.03)
    initEvt = ROOT.TLatex(); initEvt.SetTextSize(0.03)
    finalEvt = ROOT.TLatex(); finalEvt.SetTextSize(0.03)
    
    c = ROOT.TCanvas("canvas", "", 800, 800)
    c.cd()
    c.SetLogy()
    cutflow.Draw("hist&text30")
    initEvt.DrawLatexNDC(0.55, 0.8, f"initial Evts = {nTotal:.6f}")
    finalEvt.DrawLatexNDC(0.55, 0.75, f"final Evts = {nFinal:.6f}")
    eff.DrawLatexNDC(0.55, 0.7, f"efficiency = {nFinal / nTotal * 100:.4f}%")

    c.RedrawAxis()
    c.SaveAs(f"plots/{ERA}/{CHANNEL}__/cutflow_{SAMPLE}.png")
    f.Close()
