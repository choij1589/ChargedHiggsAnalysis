import ROOT

metrics_before = {
        "MHc-70_MA-65": 3.285,
        "MHc-160_MA-85": 2.431,
        "MHc-130_MA-90": 1.852,
        "MHc-100_MA-95": 1.771,
        "MHc-160_MA-120": 3.842
}
metrics_after = {
        "MHc-70_MA-65": 4.807,
        "MHc-160_MA-85": 3.126,
        "MHc-130_MA-90": 2.521,
        "MHc-100_MA-95": 2.613,
        "MHc-160_MA-120": 5.379
}

graph_before = ROOT.TGraph()
for masspoint, metric in metrics_before.items():
    mA = float(masspoint.split("_")[1].split("-")[1])
    graph_before.AddPoint(mA, metric)

graph_after = ROOT.TGraph()
for masspoint, metric in metrics_after.items():
    mA = float(masspoint.split("_")[1].split("-")[1])
    graph_after.AddPoint(mA, metric)

graph_ratio = ROOT.TGraph()
for masspoint in metrics_before.keys():
    mA = float(masspoint.split("_")[1].split("-")[1])
    ratio = (metrics_after[masspoint]/ metrics_before[masspoint])-1
    graph_ratio.AddPoint(mA, ratio)

graph_after.GetXaxis().SetLabelSize(0)
graph_after.GetYaxis().SetRangeUser(1., 7.)
graph_after.GetYaxis().SetTitle("Expected Significance")
graph_after.SetLineColor(ROOT.kBlack)
graph_after.SetLineWidth(2)

graph_before.SetLineColor(ROOT.kBlue)
graph_before.SetLineWidth(2)

graph_ratio.GetXaxis().SetLabelSize(0.1)
graph_ratio.GetXaxis().SetTitle("M_{A}")
graph_ratio.GetXaxis().SetTitleSize(0.1)
graph_ratio.GetYaxis().SetRangeUser(0.1, 0.6)
graph_ratio.GetYaxis().SetLabelSize(0.08)
graph_ratio.GetYaxis().SetTitle("Improvement")
graph_ratio.GetYaxis().SetTitleSize(0.1)
graph_ratio.GetYaxis().SetTitleOffset(0.32)
graph_ratio.GetYaxis().CenterTitle()
graph_ratio.SetLineWidth(2)

legend = ROOT.TLegend(0.55, 0.75, 0.90, 0.85)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.AddEntry(graph_before, "before optim.", "l")
legend.AddEntry(graph_after, "after optim.",  "l")

c = ROOT.TCanvas("c", "", 800, 800)
pad_up = ROOT.TPad("pad_up", "", 0, 0.25, 1, 1)
pad_down = ROOT.TPad("pad_down", "", 0, 0, 1, 0.25)

pad_up.SetBottomMargin(0.01)
pad_down.SetTopMargin(0.01)
pad_down.SetBottomMargin(0.25)
pad_down.SetGrid(True)

pad_up.cd()
graph_after.Draw()
graph_before.Draw("same")
legend.Draw("same")

text = ROOT.TLatex()
text.SetTextSize(0.05)
text.SetTextFont(61)
text.DrawLatexNDC(0.17, 0.8, "CMS")

text.SetTextSize(0.04)
text.SetTextFont(52);
text.DrawLatexNDC(0.17, 0.75, "Work in progress");

text.SetTextSize(0.04)
text.SetTextFont(42)
text.DrawLatexNDC(0.75, 0.912, "L_{int} = 59.8 fb^{-1}")

pad_down.cd()
graph_ratio.Draw()

c.cd()
pad_up.Draw()
pad_down.Draw()
c.SaveAs("improvement.png")

