import os
import argparse
import ROOT

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--measure", required=True, type=str, help="muon / electron")
parser.add_argument("--eta", required=True, type=int, help="eta bin no.")
args = parser.parse_args()

ERA = args.era
MEASURE = args.measure
ETABIN = args.eta

ptCorr_bins = []
abseta_bins = []
if MEASURE == "muon":
    ptCorr_bins = [10., 15., 20., 30., 50., 100.]
    abseta_bins = [0., 0.9, 1.6, 2.4]
elif MEASURE == "electron":
    ptCorr_bins = [10., 15., 20., 25., 35., 50., 100.]
    abseta_bins = [0., 0.8, 1.579, 2.5]
else:
    raise NameError(f"Wrong measure {MEASURE}")

# get fake rates
file_path = f"results/{ERA}/ROOT/{MEASURE}/fakerate.root"
f = ROOT.TFile.Open(file_path)
h = f.Get("fakerate"); h.SetDirectory(0)
h_prUp = f.Get("fakerate_PromptNormUp"); h_prUp.SetDirectory(0)
h_prDown = f.Get("fakerate_PromptNormDown"); h_prDown.SetDirectory(0)
h_jetUp = f.Get("fakerate_MotherJetPtUp"); h_jetUp.SetDirectory(0)
h_jetDown = f.Get("fakerate_MotherJetPtDown"); h_jetDown.SetDirectory(0)
h_btag = f.Get("fakerate_RequireHeavyTag"); h_btag.SetDirectory(0)
f.Close()

# make projections
h_proj_central = h.ProjectionY("central", ETABIN, ETABIN)
h_proj_prUp = h_prUp.ProjectionY("prUp", ETABIN, ETABIN)
h_proj_prDown = h_prDown.ProjectionY("prDown", ETABIN, ETABIN)
h_proj_jetUp = h_jetUp.ProjectionY("jetUp", ETABIN, ETABIN)
h_proj_jetDown = h_jetDown.ProjectionY("jetDown", ETABIN, ETABIN)
h_proj_btag = h_btag.ProjectionY("btag", ETABIN, ETABIN)

# make ratio plots for each systematic sources
ratio_total = h_proj_central.Clone("total")
for bin in range(1, ratio_total.GetNbinsX()+1):
    error = ratio_total.GetBinError(bin) / ratio_total.GetBinContent(bin)
    ratio_total.SetBinContent(bin, 0.)
    ratio_total.SetBinError(bin, error)
    
# promptNorm
ratio_prUp = h_proj_central.Clone("PromptNormUp")
for bin in range(1, ratio_prUp.GetNbinsX()+1):
    content = (h_proj_prUp.GetBinContent(bin) - h_proj_central.GetBinContent(bin))/h_proj_central.GetBinContent(bin)
    ratio_prUp.SetBinContent(bin, content)

# promptNormDown
ratio_prDown = h_proj_central.Clone("PromptNormDown")
for bin in range(1, ratio_prDown.GetNbinsX()+1):
    content = (h_proj_prDown.GetBinContent(bin) - h_proj_central.GetBinContent(bin))/h_proj_central.GetBinContent(bin)
    ratio_prDown.SetBinContent(bin, content)
    
# JetPtUp
ratio_jetUp = h_proj_central.Clone("MotherJetPtUp")
for bin in range(1, ratio_jetUp.GetNbinsX()+1):
    content = (h_proj_jetUp.GetBinContent(bin) - h_proj_central.GetBinContent(bin))/h_proj_central.GetBinContent(bin)
    ratio_jetUp.SetBinContent(bin, content)
    
# JetPtDown
ratio_jetDown = h_proj_central.Clone("MotherJetPtDown")
for bin in range(1, ratio_jetDown.GetNbinsX()+1):
    content = (h_proj_jetDown.GetBinContent(bin) - h_proj_central.GetBinContent(bin))/h_proj_central.GetBinContent(bin)
    ratio_jetDown.SetBinContent(bin, content)
    
# RequireHeavyTag
ratio_btag = h_proj_central.Clone("RequireHeavyTag")
for bin in range(1, ratio_btag.GetNbinsX()+1):
    content = (h_proj_btag.GetBinContent(bin) - h_proj_central.GetBinContent(bin))/h_proj_central.GetBinContent(bin)
    ratio_btag.SetBinContent(bin, content)
    
# set up ratios
ratio_total.SetStats(0)
ratio_total.SetFillColorAlpha(12, 0.6)
ratio_total.SetFillStyle(3144)
ratio_total.GetXaxis().SetTitle("p_{T}^{corr}")
ratio_total.GetXaxis().SetRangeUser(10., 50.)
ratio_total.GetYaxis().SetTitle("#Delta fr / fr")
ratio_total.GetYaxis().CenterTitle()
ratio_total.GetYaxis().SetRangeUser(-1.5, 1.5)

ratio_prUp.SetMarkerStyle(8)
ratio_prUp.SetMarkerSize(2)
ratio_prUp.SetMarkerColor(ROOT.kGreen)
ratio_prDown.SetMarkerStyle(8)
ratio_prDown.SetMarkerSize(2)
ratio_prDown.SetMarkerColor(ROOT.kGreen)

ratio_jetUp.SetMarkerStyle(8)
ratio_jetUp.SetMarkerSize(2)
ratio_jetUp.SetMarkerColor(ROOT.kBlue)
ratio_jetDown.SetMarkerStyle(8)
ratio_jetDown.SetMarkerSize(2)
ratio_jetDown.SetMarkerColor(ROOT.kBlue)

ratio_btag.SetMarkerStyle(8)
ratio_btag.SetMarkerSize(2)
ratio_btag.SetMarkerColor(ROOT.kBlack)

# prepare canvas and legend
def setInfoTo(text: ROOT.TLatex):
    text.SetTextSize(0.035)
    text.SetTextFont(42)

def setLogoTo(text: ROOT.TLatex):
    text.SetTextSize(0.04)
    text.SetTextFont(61)
    
def setWorkInProgressTo(text: ROOT.TLatex):
    text.SetTextSize(0.035)
    text.SetTextFont(52)
    
def setExtraInfoTo(text: ROOT.TLatex):
    text.SetTextSize(0.05)
    text.SetTextFont(42)

canvas = ROOT.TCanvas("c", "", 1600, 1200)
canvas.SetLeftMargin(0.1)
canvas.SetRightMargin(0.08)
canvas.SetTopMargin(0.1)
canvas.SetBottomMargin(0.12)

legend = ROOT.TLegend(0.67, 0.65, 0.9, 0.85)
legend.SetFillStyle(0)
legend.SetBorderSize(0)

# add to legend
legend.AddEntry(ratio_prUp, "PromptNorm", "p")
legend.AddEntry(ratio_jetUp, "MotherJetPt", "p")
legend.AddEntry(ratio_btag, "RequireHeavyTag", "p")
legend.AddEntry(ratio_total, "Total", "f")

canvas.cd()
ratio_total.Draw("e2&f")
ratio_prUp.Draw("p&hist&same")
ratio_prDown.Draw("p&hist&same")
ratio_jetUp.Draw("p&hist&same")
ratio_jetDown.Draw("p&hist&same")
ratio_btag.Draw("p&hist&same")
legend.Draw("same")

text = ROOT.TLatex()
setInfoTo(text); text.DrawLatexNDC(0.835, 0.91, "(13TeV)")
setLogoTo(text); text.DrawLatexNDC(0.1, 0.91, "CMS")
setWorkInProgressTo(text); text.DrawLatexNDC(0.18, 0.91, "Work in progress")
setExtraInfoTo(text); text.DrawLatexNDC(0.15, 0.80, f"{abseta_bins[ETABIN-1]} < |#eta| < {abseta_bins[ETABIN]}")

save_path = f"results/{ERA}/plots/{MEASURE}/systematcis_etabin{ETABIN}.png"
os.makedirs(os.path.dirname(save_path), exist_ok=True)
canvas.SaveAs(save_path)
