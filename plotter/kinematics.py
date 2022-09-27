import os
from ROOT import TCanvas, TLegend, TLatex
from ROOT import THStack

class Canvas():
    lumi_info = {
            "2016preVFP": "L^{int} = 19.5 fb^{-1} (13TeV)",
            "2016postVFP": "L^{int} = 16.8 fb^{-1} (13TeV)",
            "2017": "L^{int} = 41.5 fb^{-1} (13TeV) ",
            "2018": "L^{int} = 59.8 fb^{-1} (13TeV)"
        }
    def __init__(self, config=None):
        self.config = config
        
        self.logy = "logY" in self.config.keys()
        self.maximum = 0.
        
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
        self.legend = None
        
    def draw_signals(self, hists, colors):
        self.signals = hists
        for hist in self.signals.values():
            hist.SetStats(0)
        
        # Rebin
        if "rebin" in self.config.keys():
            rebin = self.config['rebin']
            for hist in self.signals.values():
                hist.Rebin(rebin)
                
        # Set colors
        for hist in self.signals.values():
            color = colors[hist.GetName()]
            hist.SetLineColor(color)
            hist.SetLineWidth(2)
            hist.SetMarkerColor(color)
        
        # X axis
        x_range = None
        if "x_range" in self.config.keys():
            x_range = self.config['x_range']
        for hist in self.signals.values():
            hist.GetXaxis().SetTitle(self.config['x_title'])
            hist.GetXaxis().SetTitleSize(0.04)
            hist.GetXaxis().SetTitleOffset(1.0)
            hist.GetXaxis().SetLabelSize(0.04)
            if not x_range is None:
                hist.GetXaxis().SetRangeUser(x_range[0], x_range[1]) 
                
    def draw_backgrounds(self, hists, colors):
        self.backgrounds = hists
        for hist in self.backgrounds.values():
            hist.SetStats(0)
        
        # Rebin
        if "rebin" in self.config.keys():
            rebin = self.config['rebin']
            for hist in self.backgrounds.values():
                hist.Rebin(rebin)
        
        # Set colors
        for hist in self.backgrounds.values():
            color = colors[hist.GetName()]
            hist.SetFillColorAlpha(color, 0.2)
                
        # make stack and systematics
        for hist in self.backgrounds.values():
            self.stack.Add(hist)
            if self.systematics is None:
                self.systematics = hist.Clone("syst")
            else:
                self.systematics.Add(hist)
        
        self.stack.Draw() 
        # x axis
        x_range = None
        if "x_range" in self.config.keys():
            x_range = self.config['x_range']
        
        self.stack.GetHistogram().SetTitle(self.config['x_title'])
        self.stack.GetHistogram().GetXaxis().SetTitleOffset(1.0)
        self.stack.GetHistogram().GetXaxis().SetTitleSize(0.04)
        self.stack.GetHistogram().GetXaxis().SetLabelSize(0.04)
        if not x_range is None:
            self.stack.GetHistogram().GetXaxis().SetRangeUser(x_range[0], x_range[1])

        # y axis
        self.stack.GetHistogram().GetYaxis().SetTitle(self.config['y_title'])
        self.stack.GetHistogram().GetYaxis().SetTitleOffset(1.0)
        self.stack.GetHistogram().GetYaxis().SetTitleSize(0.04)
        self.stack.GetHistogram().GetYaxis().SetLabelSize(0.04)
        self.maximum = self.stack.GetHistogram().GetMaximum()
        if self.logy:
            self.stack.GetHistogram().GetYaxis().SetRangeUser(1., self.maximum*10.)
        else:
            self.stack.GetHistogram().GetYaxis().SetRangeUser(0., self.maximum*2.)
        
        self.systematics.SetStats(0)
        self.systematics.SetFillColorAlpha(12, 0.6)
        self.systematics.SetFillStyle(3144)
        self.systematics.GetXaxis().SetLabelSize(0)
        
    def draw_legend(self):
        self.legend = TLegend(0.6, 0.6, 0.90, 0.85)
        self.legend.SetFillStyle(0)
        self.legend.SetBorderSize(0)
        # self.legend.SetNColumns(2)
        for hist in self.backgrounds.values():
            self.legend.AddEntry(hist, hist.GetName(), "f")
        self.legend.AddEntry(self.systematics, "stat+syst", "f")
        for hist in self.signals.values():
            self.legend.AddEntry(hist, hist.GetName(), "lep")
            
    def finalize(self, era):
        if self.logy: self.cvs.SetLogy()
        
        for hist in self.signals.values():
            if self.logy:
                hist.GetYaxis().SetRangeUser(1., self.maximum*10)
            else:
                hist.GetYaxis().SetRangeUser(0., self.maximum*2.)
        
        self.cvs.cd()
        for hist in self.signals.values():
            hist.Draw("hist") 
        self.stack.Draw("hist&pfc&same")
        self.systematics.Draw("e2&f&same")
        for hist in self.signals.values():
            hist.Draw("hist&same")
        self.legend.Draw()
        self.lumi.DrawLatexNDC(0.62, 0.91, self.lumi_info[era])
        self.cms.DrawLatexNDC(0.15, 0.83, "CMS")
        self.preliminary.DrawLatexNDC(0.15, 0.78, "Work in progress") 
        self.cvs.RedrawAxis()

    def draw(self):
        self.cvs.Draw()
        
    def savefig(self, name):
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        self.cvs.SaveAs(name)
