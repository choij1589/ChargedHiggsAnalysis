import ROOT
from CombineHarvester.CombineTools.plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
 
# Style and pads
ERA = "2018"
CHANNEL = "Skim3Mu"
METHOD = "Shape"


lumiDict = {
        "2016preVFP": "19.5",
        "2016postVFP": "16.8",
        "2017": "41.5",
        "2018": "59.8",
        "FullRun2": "137.5"
}


ModTDRStyle()
canv = ROOT.TCanvas('limit.{}.{}.HybridNew.{}'.format(ERA, CHANNEL, METHOD))
pads = OnePad()

# Get limit TGraphs as a dictionary
graphs_gnn = StandardLimitsFromJSONFile('../HiggsCombineV4/limits/limits.{}.{}.HybridNew.GNNOptim.json'.format(ERA, CHANNEL))
graphs_cnc = StandardLimitsFromJSONFile('../HiggsCombineV4/limits/limits.{}.{}.HybridNew.CutNCount.json'.format(ERA, CHANNEL))
graphs_shape = StandardLimitsFromJSONFile('../HiggsCombineV4/limits/limits.{}.{}.HybridNew.Shape.json'.format(ERA, CHANNEL))

if METHOD == "CutNCount":
    graphs = graphs_cnc
elif METHOD == "Shape":
    graphs = graphs_shape
elif METHOD == "GNNOptim":
    graphs = graphs_gnn
else:
    print("Wrong method {}".format(METHOD))
    exit(1)

graphs_thres10 = StandardLimitsFromJSONFile('limits/limits.{}.{}.HybridNew.Shape.json'.format(ERA, CHANNEL))

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
DrawLimitBand(pads[0], graphs, draw=['exp2', 'exp1', 'exp0'], legend=legend)

comp = graphs_thres10["exp0"]
comp.SetLineColor(ROOT.kViolet)
comp.SetLineWidth(2)
comp.SetLineStyle(4)
comp.Draw("LSAME")
legend.AddEntry(comp, "Expected (#theta = 10)", "L")

# Redraw central values
graphs["exp0"].Draw("LSAME")
#graphs["obs"].Draw("PLSAME")
legend.Draw()
 
# Re-draw the frame and tick marks
pads[0].RedrawAxis()
pads[0].GetFrame().Draw()
#pads[0].SetLogy() 
# Adjust the y-axis range such that the maximum graph value sits 25% below
# the top of the frame. Fix the minimum to zero.
#FixBothRanges(pads[0], 0, 0, GetPadYMax(pads[0]), 0.25)
FixBothRanges(pads[0], 0, 0, 10, 0.25)

# Standard CMS logo
DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.2, '', 0.8)

# Title
DrawTitle(pads[0], "L_{int} = "+ lumiDict[ERA] + " fb^{-1}", 3)
canv.Print('.png')
