import ROOT
from CombineHarvester.CombineTools.plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
 
# Style and pads
ModTDRStyle()
canv = ROOT.TCanvas('limit.HybridNew', 'limit.HybridNew')
pads = OnePad()

# Get limit TGraphs as a dictionary
graphs = StandardLimitsFromJSONFile('limits.2018.Skim3Mu.HybridNew.withcut.json')
graphs_cnc = StandardLimitsFromJSONFile('limits.2018.Skim3Mu.HybridNew.CnC.json')
graphs_nocut = StandardLimitsFromJSONFile('limits.2018.Skim3Mu.HybridNew.nocut.json')

# Create an empty TH1 from the first TGraph to serve as the pad axis and frame
axis = CreateAxisHist(graphs.values()[0])
axis.GetXaxis().SetTitle('M(#mu^{+}#mu^{-}) (GeV)')
axis.GetYaxis().SetTitle('95% CL limit on #sigma_{sig} [fb]')
pads[0].cd()
axis.Draw('axis')
 
# Create a legend in the top left
legend = PositionedLegend(0.3, 0.2, 3, 0.015)
 
# Set the standard green and yellow colors and draw
StyleLimitBand(graphs)
DrawLimitBand(pads[0], graphs, legend=legend)
cnc = graphs_cnc["exp0"]
cnc.SetLineColor(ROOT.kGray)
cnc.SetLineWidth(2)
cnc.Draw("LSAME")
legend.AddEntry(cnc, "Expected (cut and count)", "L")

nocut = graphs_nocut["exp0"]
nocut.SetLineColor(ROOT.kInvertedDarkBodyRadiator)
nocut.SetLineWidth(2)
nocut.Draw("LSAME")
legend.AddEntry(nocut, "Expected (no GNN optim)", "L") 

# Redraw central values
graphs["exp0"].Draw("LSAME")
graphs["obs"].Draw("PLSAME")
legend.Draw()
 
# Re-draw the frame and tick marks
pads[0].RedrawAxis()
pads[0].GetFrame().Draw()
 
# Adjust the y-axis range such that the maximum graph value sits 25% below
# the top of the frame. Fix the minimum to zero.
#FixBothRanges(pads[0], 0, 0, GetPadYMax(pads[0]), 0.25)
FixBothRanges(pads[0], 0, 0, 15, 0.25)

# Standard CMS logo
DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.2, '', 0.8)

# Title
DrawTitle(pads[0], "L_{int} = 59.8 fb^{-1}", 3)

canv.Print('.png')
