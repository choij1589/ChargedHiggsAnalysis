import os
from ROOT import TCanvas, TLegend, TLatex
from ROOT import THStack
from MetaInfo.AllEras import LumiInfo

class KinematicCanvas():
    def __init__(self, config):
        self.config = config
        
        # initialize default settings
        self.cvs = TCanvas("c", "", 720, 900)
        self.lumi = TLatex()
        self.lumi.SetTextSize(0.035)
        self.lumi.SetTextFont(42)
        self.cms = TLatex()
        self.cms.SetTextSize(0.04)
        self.cms.SetTextFont(61)
        self.preliminary = TLatex()
        self.preliminary.SetTextSize(0.035)
        self.preliminary.SetTextFont(52)
        
        self.signals = None
        self.backgrounds = None
        self.stack = THStack("stack", "")
        self.systematics = None
        self.legend = TLegend(0.6, 0.6, 0.9, 0.85)
        self.legend.SetFillStyle(0)
        self.legend.SetBorderSize(0)
        
        # optional settings
        self.logy = "logY" in self.config.keys()
        self.lumiString = ""
        if "era" in config.keys():
            era = config['era']
            self.lumiString = "L_{int} ="+f" {LumiInfo[era]}"+" fb^{-1} (13TeV)"
    
    def drawSignals(self, hists, colors):
        self.signals = hists
        
        # color
        for hist in self.signals.values(): 
            hist.SetStats(0)
            color = colors[hist.GetName()]
            hist.SetLineColor(color)
            hist.SetLineWidth(2)
            hist.SetMarkerColor(color)
        
        # rebin
        if "rebin" in self.config.keys():
            for hist in self.signals.values(): hist.Rebin(self.config['rebin'])
        
        # X axis
        xRange = None
        if "xRange" in self.config.keys():
            xRange = self.config['xRange']
        for hist in self.signals.values():
            hist.GetXaxis().SetTitle(self.config['xTitle'])
            hist.GetXaxis().SetTitleSize(0.04)
            hist.GetXaxis().SetTitleOffset(1.0)
            hist.GetXaxis().SetLabelSize(0.04)
            if xRange:
                hist.GetXaxis().SetRangeUser(xRange[0], xRange[1])
        
    def drawBackgrounds(self, hists, colors):
        self.backgrounds = hists
        
        # color
        for hist in self.backgrounds.values():
            hist.SetStats(0)
            color = colors[hist.GetName()]
            print(color)
            hist.SetFillColor(color)
            
        # rebin
        if "rebin" in self.config.keys():
            for hist in self.backgrounds.values(): hist.Rebin(self.config['rebin']) 
            
        # make stack and systematics
        for hist in self.backgrounds.values():
            self.stack.Add(hist)
            if self.systematics is None:
                self.systematics = hist.Clone("syst")
            else:
                self.systematics.Add(hist)
        self.stack.Draw()   # to use self.stack.GetHistogram()
        
        # X axis
        xRange = None
        if "xRange" in self.config.keys():
            xRange = self.config['xRange']
        
        self.stack.GetHistogram().SetTitle(self.config['xTitle'])
        self.stack.GetHistogram().GetXaxis().SetTitleOffset(1.0)
        self.stack.GetHistogram().GetXaxis().SetTitleSize(0.04)
        self.stack.GetHistogram().GetXaxis().SetLabelSize(0.04)
        if xRange:
            self.stack.GetHistogram().GetXaxis().SetRangeUser(xRange[0], xRange[1])
        
        maximum = self.stack.GetHistogram().GetMaximum()
        if self.logy:
            self.stack.GetHistogram().GetYaxis().SetRangeUser(1., maximum*50.)
            if self.signals:
                for hist in self.signals.values():
                    hist.GetYaxis().SetRangeUser(1., maximum*50.)
        else:
            self.stack.GetHistogram().GetYaxis().SetRangeUser(0., maximum*2.)
            if self.signals:
                for hist in self.signals.values():
                    hist.GetYaxis().SetRangeUser(0., maximum*2.)
            
        self.systematics.SetStats(0)
        self.systematics.SetFillColorAlpha(12, 0.6)
        self.systematics.SetFillStyle(3144)
        self.systematics.GetXaxis().SetLabelSize(0)
        
    def drawLegend(self):
        for hist in list(self.backgrounds.values())[::-1]:
            self.legend.AddEntry(hist, hist.GetName(), "f")
        self.legend.AddEntry(self.systematics, "stat+syst", "f")
        for hist in self.signals.values():
            self.legend.AddEntry(hist, hist.GetName(), "lep")
        
    def finalize(self):
        if self.logy: self.cvs.SetLogy()
        self.cvs.cd()
        list(self.signals.values())[0].Draw("hist")
        self.stack.Draw("hist&pfc&same")
        self.systematics.Draw("e2&f&same")
        for hist in self.signals.values():
            hist.Draw("hist&same")
        self.legend.Draw()
        self.lumi.DrawLatexNDC(0.6, 0.91, self.lumiString)
        self.cms.DrawLatexNDC(0.15, 0.83, "CMS")
        self.preliminary.DrawLatexNDC(0.15, 0.78, "Work in progress") 
        self.cvs.RedrawAxis()
        
    def draw(self):
        self.cvs.Draw()
        
    def savefig(self, name):
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        self.cvs.SaveAs(name)
        
            
            
                