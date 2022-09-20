import os
from ROOT import TCanvas, TPad, TLegend, TLatex
from ROOT import THStack


class Canvas():
    def __init__(self, config=None):
        #super(Canvas, self).__init__()
        self.config = config

        self.cvs = TCanvas("c", "", 720, 900)
        self.pad_up = TPad("up", "", 0, 0.25, 1, 1)
        self.pad_up.SetBottomMargin(0.02)
        self.pad_down = TPad("down", "", 0, 0, 1, 0.25)
        self.pad_down.SetGrid(True)
        self.pad_down.SetTopMargin(0.08)
        self.pad_down.SetBottomMargin(0.3)

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
        self.data = None
        self.predictions = None
        self.stack = THStack("stack", "")
        self.systematics = None
        self.ratio = None
        self.ratio_syst = None
        self.legend = None

    def draw_distributions(self, hists, colors):
        self.histograms = hists
        for name, hist in self.histograms.items():
            hist.SetStats(0)

        if "rebin" in self.config.keys():
            rebin = self.config['rebin']
            for hist in self.histograms.values():
                hist.Rebin(rebin)

        # Set colors
        for hist in self.histograms.values():
            color = colors[hist.GetName()]
            hist.SetFillColorAlpha(color, 0.2)

        # x axis
        for hist in self.histograms.values():
            hist.GetXaxis().SetLabelSize(0)
        if "x_range" in self.config.keys():
            for hist in self.histograms.values():
                hist.GetXaxis().SetRangeUser(self.config["x_range"][0],
                                             self.config["x_range"][1])

        # y axis
        maximum = 0.
        for hist in self.histograms.values():
            maximum = max(maximum, hist.GetMaximum())
        setLogY = "logY" in self.config.keys()
        for hist in self.histograms.values():
            if setLogY:
                hist.GetYaxis().SetRangeUser(1, maximum*10.)
            else:
                hist.GetYaxis().SetRangeUser(0, maximum*2.)

        self.data, *self.predictions = self.histograms.values()
        self.data.SetTitle("")
        self.data.GetYaxis().SetTitleOffset(1.5)
        self.data.GetYaxis().SetLabelSize(0.035)
        if "y_title" in self.config.keys():
            self.data.GetYaxis().SetTitle(self.config["y_title"])
        self.data.SetMarkerStyle(8)
        self.data.SetMarkerSize(0.5)
        self.data.SetMarkerColor(1)

        # legend setting?
        # stack
        for hist in self.predictions:
            self.stack.Add(hist)
            if self.systematics == None:
                self.systematics = hist.Clone("syst")
            else:
                self.systematics.Add(hist)
        self.stack.Draw()
        self.stack.GetHistogram().GetXaxis().SetLabelSize(0)
        self.systematics.SetStats(0)
        self.systematics.SetFillColorAlpha(12, 0.6)
        self.systematics.SetFillStyle(3144)
        self.systematics.GetXaxis().SetLabelSize(0)

        self.pad_up.cd()
        self.data.Draw("p&hist")
        self.stack.Draw("hist&pfc&same")
        self.systematics.Draw("e2&f&same")
        self.data.Draw("p&hist&same")
        self.data.Draw("e1&same")

    def draw_ratio(self):
        self.ratio = self.data.Clone("ratio")
        self.ratio.Divide(self.systematics)
        self.ratio_syst = self.ratio.Clone("ratio_syst")

        self.ratio.SetStats(0)
        self.ratio.SetTitle("")

        # x axis
        x_title = self.config["x_title"]
        self.ratio.GetXaxis().SetTitle(x_title)
        self.ratio.GetXaxis().SetTitleSize(0.1)
        self.ratio.GetXaxis().SetTitleOffset(0.9)
        self.ratio.GetXaxis().SetLabelSize(0.08)

        # y axis
        self.ratio.GetYaxis().SetRangeUser(0.5, 1.5)
        if "ratio" in self.config.keys():
            bin_down = self.config['ratio'][0]
            bin_up = self.config['ratio'][1]
            self.ratio.GetYaxis().SetRangeUser(bin_down, bin_up)
        self.ratio.GetYaxis().SetTitle("Data / Pred")
        self.ratio.GetYaxis().CenterTitle()
        self.ratio.GetYaxis().SetTitleSize(0.08)
        self.ratio.GetYaxis().SetTitleOffset(0.5)
        self.ratio.GetYaxis().SetLabelSize(0.08)

        # syst
        self.ratio_syst.SetStats(0)
        self.ratio_syst.SetFillColorAlpha(12, 0.6)
        self.ratio_syst.SetFillStyle(3144)

        self.pad_down.cd()
        self.ratio.Draw("p&hist")
        self.ratio_syst.Draw("e2&f&same")

    def draw_legend(self):
        # legend location?
        self.legend = TLegend(0.65, 0.55, 0.90, 0.80)
        self.legend.SetFillStyle(0)
        self.legend.SetBorderSize(0)
        self.legend.AddEntry(self.data, "Data", "lep")
        for hist in self.predictions:
            self.legend.AddEntry(hist, hist.GetName(), "f")
        self.legend.AddEntry(self.systematics, "stat+syst", "f")

        self.pad_up.cd()
        self.legend.Draw()

    def draw_latex(self, era):
        lumi_info = {
            "2016preVFP": "L^{int} = 19.5 fb^{-1} (13TeV)",
            "2016postVFP": "L^{int} = 16.8 fb^{-1} (13TeV)",
            "2017": "L^{int} = 41.5 fb^{-1} (13TeV) ",
            "2018": "L^{int} = 59.8 fb^{-1} (13TeV)"
        }
        # CMS texts, etc...
        self.pad_up.cd()
        self.lumi.DrawLatexNDC(0.62, 0.91, lumi_info[era])
        self.cms.DrawLatexNDC(0.15, 0.83, "CMS")
        self.preliminary.DrawLatexNDC(0.15, 0.78, "Work in progress")

    def finalize(self):
        # log
        setLogY = "logY" in self.config.keys()
        if setLogY: self.pad_up.SetLogy()
        self.cvs.cd()
        self.pad_up.Draw()
        self.pad_down.Draw()

    def draw(self):
        self.cvs.Draw()

    def savefig(self, name):
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        self.cvs.SaveAs(name)
