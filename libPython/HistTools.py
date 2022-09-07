import os
import ROOT
from ROOT import TFile, TH1D, TH2D, TH3D


class HistogramWriter():
    def __init__(self, outfile="./test.root"):
        self.hists = dict()
        self.dirs = dict()

        if not os.path.exists(os.path.dirname(outfile)):
            os.makedirs(os.path.dirname(outfile))
        self.outfile = TFile(outfile, "recreate")
        self.outfile_name = outfile

    def fill_hist(self, histkey, value, weight, n_bin, x_min, x_max):
        *directories, obj = histkey.split("/")
        dir_path = "/".join(directories)

        # change to the directory
        try:
            for i, subdir in enumerate(directories):
                mother = ROOT.gFile if i == 0 else ROOT.gDirectory
                this_dir = mother.GetDirectory(subdir)
                this_dir.cd()
        except:
            self.outfile.mkdir(dir_path)
            self.outfile.cd(dir_path)

        # now fill hist
        try:
            self.hists[histkey].Fill(value, weight)
        except:
            self.hists[histkey] = TH1D(obj, "", n_bin, x_min, x_max)
            self.hists[histkey].SetDirectory(ROOT.gDirectory)
            self.hists[histkey].Fill(value, weight)

    def fill_hist2d(self, histkey, x_value, y_value, weight, n_binx, x_min,
                    x_max, n_biny, y_min, y_max):
        *directories, obj = histkey.split("/")
        dir_path = "/".join(directories)

        # change to the directory
        try:
            for i, subdir in enumerate(directories):
                mother = ROOT.gFile if i == 0 else ROOT.gDirectory
                this_dir = mother.GetDirectory(subdir)
                this_dir.cd()
        except:
            self.outfile.mkdir(dir_path)
            self.outfile.cd(dir_path)

        # now fill hist
        try:
            self.hists[histkey].Fill(x_value, y_value, weight)
        except:
            self.hists[histkey] = TH2D(obj, "", n_binx, x_min, x_max, n_biny,
                                       y_min, y_max)
            self.hists[histkey].SetDirectory(ROOT.gDirectory)
            self.hists[histkey].Fill(x_value, y_value, weight)

    def fill_hist3d(self, histkey, x_value, y_value, z_value, weight, n_binx,
                    x_min, x_max, n_biny, y_min, y_max, n_binz, z_min, z_max):
        *directories, obj = histkey.split("/")
        dir_path = "/".join(directories)

        # change to the directory
        try:
            for i, subdir in enumerate(directories):
                mother = ROOT.gFile if i == 0 else ROOT.gDirectory
                this_dir = mother.GetDirectory(subdir)
                this_dir.cd()
        except:
            self.outfile.mkdir(dir_path)
            self.outfile.cd(dir_path)

        # not fill hist
        try:
            self.hists[histkey].Fill(x_value, y_value, z_value, weight)
        except:
            self.hists[histkey] = TH3D(obj, "", n_binx, x_min, x_max, n_biny,
                                       y_min, y_max, n_binz, z_min, z_max)
            self.hists[histkey].SetDirectory(ROOT.gDirectory)
            self.hists[histkey].Fill(x_value, y_value, z_value, weight)

    def fill_object(self, histkey, object, weight):
        self.fill_hist(histkey + "/pt", object.Pt(), weight, 1000, 0., 1000.)
        self.fill_hist(histkey + "/eta", object.Eta(), weight, 60, -3., 3.)
        self.fill_hist(histkey + "/phi", object.Phi(), weight, 64, -3.2, 3.2)
        self.fill_hist(histkey + "/mass", object.M(), weight, 1000, 0.,
                       1000.)

    def fill_muons(self, histkey, muons, weight):
        self.fill_hist(histkey + "/size", len(muons), weight, 10, 0., 10.)
        for i, muon in enumerate(muons, 1):
            this_histkey = histkey + "/" + str(i)
            self.fill_hist(this_histkey + "/pt", muon.Pt(), weight, 300, 0.,
                           300.)
            self.fill_hist(this_histkey + "/eta", muon.Eta(), weight, 50, -2.5,
                           2.5)
            self.fill_hist(this_histkey + "/phi", muon.Phi(), weight, 64, -3.2,
                           3.2)
            self.fill_hist(this_histkey + "/mass", muon.M(), weight, 20, 5.,
                           15.)

    def fill_electrons(self, histkey, electrons, weight):
        self.fill_hist(histkey + "/size", len(electrons), weight, 10, 0., 10.)
        for i, electron in enumerate(electrons, 1):
            this_histkey = histkey + "/" + str(i)
            self.fill_hist(this_histkey + "/pt", electron.Pt(), weight, 300,
                           0., 300.)
            self.fill_hist(this_histkey + "/eta", electron.Eta(), weight, 50,
                           -2.5, 2.5)
            self.fill_hist(this_histkey + "/phi", electron.Phi(), weight, 64,
                           -3.2, 3.2)
            self.fill_hist(this_histkey + "/mass", electron.M(), weight, 20,
                           5., 15.)

    def fill_jets(self, histkey, jets, weight):
        self.fill_hist(histkey + "/size", len(jets), weight, 20, 0., 20.)
        for i, jet in enumerate(jets, 1):
            this_histkey = histkey + "/" + str(i)
            self.fill_hist(this_histkey + "/pt", jet.Pt(), weight, 300, 0.,
                           300.)
            self.fill_hist(this_histkey + "/eta", jet.Eta(), weight, 50, -2.5,
                           2.5)
            self.fill_hist(this_histkey + "/phi", jet.Phi(), weight, 64, -3.2,
                           3.2)
            self.fill_hist(this_histkey + "/mass", jet.M(), weight, 20, 5.,
                           15.)
            self.fill_hist(this_histkey + "/btagScore", jet.BtagScore(),
                           weight, 100, 0., 1.)

    def close(self):
        print(f"Saving histograms in {self.outfile_name}...")

        for histkey, hist in self.hists.items():
            *directories, obs = histkey.split("/")
            for i, subdir in enumerate(directories):
                mother = self.outfile if i == 0 else ROOT.gDirectory
                mother.cd(subdir)
            # now write histogram
            hist.Write()
        self.outfile.Close()
