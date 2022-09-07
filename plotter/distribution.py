import os
from ROOT import TCanvas, TLegend, TLatex
from ROOT import THStack


class Distribution():
    def __init__(self, config=None):
        self.config = config
        self.cvs = TCanvas("c", "", 720, 800)

        self.lumi = TLatex()
        self.lumi.SetTextSize(0.035)
        self.lumi.SetTextFont(42)
        self.cms = TLatex()
        self.cms.SetTextSize(0.04)
        self.cms.SetTextFont(61)
        self.preliminary = TLatex()
        self.preliminary.SetTextSize(0.035)
        self.preliminary.SetTextFont(52)

        self.histograms = None
        self.stack = THStack("stack", "")
        self.legend = None

    def draw_distributions(self, hists, colors):
        self.histograms = hists
        for name, hist in self.histograms.items():
            hist.SetStats(0)

        # rebin
        if "rebin" in self.config.keys():
            rebin = self.config['rebin']
            for hist in self.histograms.values():
                hist.Rebin(rebin)

        # set colors
        for name, hist in self.histograms.items():
            color = colors[name]
            hist.SetFillColorAlpha(color, 0.2)

        # x axis
        x_title = self.config["x_title"]
        for hist in self.histograms.values():
            hist.GetXaxis().SetTitle(x_title)
            hist.GetXaxis().SetTitleSize(0.1)
            hist.GetXaxis().SetTitleOffset(0.9)
            hist.GetXaxis().SetLabelSize(0.08)
            if "x_range" in self.config.keys():
                left = self.config["x_range"][0]
                right = self.config["x_range"][1]
                hist.GetXaxis().SetRangeUser(left, right)

        # y axis
        maximum = 0
        for hist in self.histograms.values():
            maximum = max(maximum, hist.GetMaximum())
        y_title = self.config["y_title"]
        for hist in self.histograms.values():
            hist.GetYaxis().SetTitle(y_title)
            hist.GetYaxis().SetTitleOffset(1.5)
            hist.GetYaxis().SetLabelSize(0.035)
            hist.GetYaxis().SetRangeUser(0, maximum*2.)

        self.cvs.cd()
        for name, hist in self.histograms.items():
            self.hist.Draw("l&hist&same")

    def draw(self):
        self.cvs.Draw()

    def savefig(self, name):
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        self.cvs.SaveAs(name)
