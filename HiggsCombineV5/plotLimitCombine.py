import ROOT
from CombineHarvester.CombineTools.plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
 
# Style and pads
ERA = "FullRun2"
CHANNEL = "Skim3Mu"

lumiDict = {
        "2016preVFP": "19.5",
        "2016postVFP": "16.8",
        "2017": "41.5",
        "2018": "59.8",
        "FullRun2": "137.5"
}


ModTDRStyle()
canv = ROOT.TCanvas('limit.{}.{}.HybridNew'.format(ERA, CHANNEL))
pads = OnePad()

# Get limit TGraphs as a dictionary
graphs = StandardLimitsFromJSONFile('limits/limits.{}.{}.HybridNew.Shape.json'.format(ERA, CHANNEL))
graphs_low = StandardLimitsFromJSONFile('limits/limits.{}.{}.HybridNew.LowMass.json'.format(ERA, CHANNEL))
graphs_med = StandardLimitsFromJSONFile('limits/limits.{}.{}.HybridNew.InterMass.json'.format(ERA, CHANNEL))
graphs_high = StandardLimitsFromJSONFile('limits/limits.{}.{}.HybridNew.HighMass.json'.format(ERA, CHANNEL))


# Create an empty TH1 from the first TGraph to serve as the pad axis and frame
axis = CreateAxisHist(graphs.values()[0])
axis.GetXaxis().SetTitle('M(#mu^{+}#mu^{-}) (GeV)')
axis.GetYaxis().SetTitle('95% CL limit on #sigma_{sig} [fb]')
pads[0].cd()
axis.Draw('axis')
 
# Create a legend in the top left
legend = PositionedLegend(0.3, 0.2, 3, 0.015)
 
# Set the standard green and yellow colors and draw
StyleLimitBand(graphs_low)
StyleLimitBand(graphs_med)
StyleLimitBand(graphs_high)
DrawLimitBand(pads[0], graphs_low, draw=['exp2', 'exp1', 'exp0'])
DrawLimitBand(pads[0], graphs_med, draw=['exp2', 'exp1', 'exp0'], legend=legend)
DrawLimitBand(pads[0], graphs_high, draw=['exp2', 'exp1', 'exp0'])

leftLine = ROOT.TLine(65, 0.1, 65, 3.5);
leftLine.SetLineColor(ROOT.kBlack)
leftLine.SetLineWidth(2)
leftLine.Draw("same")

rightLine = ROOT.TLine(120, 0.1, 120, 3.5);
rightLine.SetLineColor(ROOT.kBlack)
rightLine.SetLineWidth(2)
rightLine.Draw("same")


# Redraw central values
#graphs["exp0"].Draw("LSAME")
#graphs["obs"].Draw("PLSAME")
legend.Draw()
 
# Re-draw the frame and tick marks
pads[0].RedrawAxis()
pads[0].GetFrame().Draw()
#pads[0].SetLogy() 
# Adjust the y-axis range such that the maximum graph value sits 25% below
# the top of the frame. Fix the minimum to zero.
#FixBothRanges(pads[0], 0, 0, GetPadYMax(pads[0]), 0.25)
FixBothRanges(pads[0], 0, 0, 7, 0.25)

# Standard CMS logo
DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.2, '', 0.8)

# Title
DrawTitle(pads[0], "L_{int} = "+ lumiDict[ERA] + " fb^{-1}", 3)
canv.Print('.png')
