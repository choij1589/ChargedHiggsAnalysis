import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from math import sqrt, log
import pickle
import joblib

import ROOT

from helper.fitResults import getFitSigmaValue
ROOT.gROOT.SetBatch(True)

#### parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--channel", required=True, type=str, help="channel")
args = parser.parse_args()

#### global variables
mA = int(args.signal.split("_")[1].split("-")[1])
sigma = getFitSigmaValue(args.era, args.channel, mA)

outPlotDir = f"results/{args.era}/{args.channel}__GNNOptim__/{args.signal}/plots"
os.makedirs(outPlotDir, exist_ok=True)

#### helper functions
def load_dataset(process, max_window=5):
    events = []
    f = ROOT.TFile(f"samples/{args.era}/{args.channel}__GraphNet__/{args.signal}/{process}.root")
    tree = f.Get(f"{process}_Central")
    for idx, evt in enumerate(tree, start=1):
        condition = (mA - max_window*sigma < evt.mass1 < mA + max_window*sigma) or (mA - max_window*sigma < evt.mass2 < mA + max_window*sigma)
        if not condition:
            continue
        events.append([evt.scoreX, evt.scoreY, evt.scoreZ, evt.weight, int(process == args.signal)])
    if len(events) == 0:
        return None
    return np.array(events)

def plotInput(h_sig, h_bkg, title):
    h_sig.SetLineColor(ROOT.kBlack)
    h_bkg.SetLineColor(ROOT.kRed)

    h_sig.SetLineWidth(2)
    h_bkg.SetLineWidth(2)
    h_sig.Scale(1./h_sig.Integral())
    h_bkg.Scale(1./h_bkg.Integral())

    h_sig.SetStats(0)
    h_sig.SetTitle(title)
    h_sig.GetXaxis().SetTitle("score")
    h_sig.GetYaxis().SetTitle("events")

    c = ROOT.TCanvas()
    c.SetLogy()
    c.cd()
    h_sig.Draw("hist")
    h_bkg.Draw("hist&same")
    c.SaveAs(f"{outPlotDir}/{title}.png")

def train(max_window, n_estimator=50):
    print(f"@@@@ Start training with max_window = {max_window}, n_estimator = {n_estimator}...")
    #### load dataset
    events_sig = load_dataset(args.signal, max_window)
    events_bkg = []
    for bkg in ["diboson", "ttX", "conversion", "nonprompt", "others"]:
        events_temp = load_dataset(bkg, max_window)
        if events_temp is None:
            continue
        events_bkg.append(events_temp)
    events_bkg = np.concatenate(events_bkg, axis=0)
    
    ## scale signal so that the total events of signals and backgrounds are the same
    hX_sig = ROOT.TH1D("hX_sig", "", 100, 0., 1.)
    hY_sig = ROOT.TH1D("hY_sig", "", 100, 0., 1.)
    hZ_sig = ROOT.TH1D("hZ_sig", "", 100, 0., 1.)
    hX_bkg = ROOT.TH1D("hX_bkg", "", 100, 0., 1.)
    hY_bkg = ROOT.TH1D("hY_bkg", "", 100, 0., 1.)
    hZ_bkg = ROOT.TH1D("hZ_bkg", "", 100, 0., 1.)

    for evt in events_sig:
        scoreX, scoreY, scoreZ, weight = tuple(evt[:4])
        hX_sig.Fill(scoreX, weight)
        hY_sig.Fill(scoreY, weight)
        hZ_sig.Fill(scoreZ, weight)

    for evt in events_bkg:
        scoreX, scoreY, scoreZ, weight = tuple(evt[:4])
        hX_bkg.Fill(scoreX, weight)
        hY_bkg.Fill(scoreY, weight)
        hZ_bkg.Fill(scoreZ, weight)

    print("@@@@ Scaling signal...")
    sigScaleFactor = hX_bkg.Integral() / hX_sig.Integral()
    print(f"@@@@ nSig = {hX_sig.Integral():.3f}")
    print(f"@@@@ nBkg = {hX_bkg.Integral():.3f}")
    print(f"@@@@ scale factor = {sigScaleFactor}")
    events_sig[:, 3] = events_sig[:, 3]*sigScaleFactor

    print("@@@@ Saving input distributions...")
    plotInput(hX_sig, hX_bkg, "scoreX")
    plotInput(hY_sig, hY_bkg, "scoreY")
    plotInput(hZ_sig, hZ_bkg, "scoreZ")

    #### preprocessing
    events_bkg = shuffle(events_bkg, random_state=42)
    events = np.concatenate([events_sig, events_bkg], axis=0)
    events = shuffle(events, random_state=42)

    X, weights, y = events[:, :3], events[:, 3], events[:, 4]
    X_train, X_test, y_train, y_test, sw_train, sw_test = train_test_split(X, y, weights, test_size=0.4, random_state=42)
    ## train GBclassifier
    print("@@@@ Start training...")
    clf = GradientBoostingClassifier(n_estimators=n_estimator, max_depth=3)
    clf.fit(X_train, y_train, sample_weight=sw_train)
    print("@@@@ feature importance")
    print(f"@@@@ scoreX = {clf.feature_importances_[0]}")
    print(f"@@@@ scoreY = {clf.feature_importances_[1]}")
    print(f"@@@@ scoreZ = {clf.feature_importances_[2]}")

    ## checck overfitting
    print("@@@@ Check overfitting...")
    hSigTrain = ROOT.TH1D("hSigTrain", "", 100, 0., 1.)
    hBkgTrain = ROOT.TH1D("hBkgTrain", "", 100, 0., 1.)
    hSigTest = ROOT.TH1D("hSigTest", "", 100, 0., 1.)
    hBkgTest = ROOT.TH1D("hBkgTest", "", 100, 0., 1.)

    y_pred = clf.predict_proba(X_train)
    for score, weight, label in zip(y_pred, sw_train, y_train):
        if label == 0: hBkgTrain.Fill(score[1], weight)
        else: hSigTrain.Fill(score[1], weight)

    y_pred = clf.predict_proba(X_test)
    for score, weight, label in zip(y_pred, sw_test, y_test):
        if label == 0: hBkgTest.Fill(score[1], weight)
        else: hSigTest.Fill(score[1], weight)

    ksProbSig = hSigTrain.KolmogorovTest(hSigTest, option="X")
    ksProbBkg = hBkgTrain.KolmogorovTest(hBkgTest, option="X")
    print(f"@@@@ ksProbSig = {ksProbSig}")
    print(f"@@@@ ksProbBkg = {ksProbBkg}")
    if ksProbSig < 0.05 or ksProbBkg < 0.05:
        print(f"@@@@ failed training with max_window {max_window}, n_estimator {n_estimator}")
        return False
    
    print("@@@@ save results...")
    hSigTrain.SetLineColor(ROOT.kBlack)
    hBkgTrain.SetLineColor(ROOT.kBlue)
    hSigTrain.SetLineWidth(2)
    hBkgTrain.SetLineWidth(2)
    hSigTest.SetMarkerStyle(20)
    hBkgTest.SetMarkerStyle(20)
    hSigTest.SetMarkerSize(1)
    hBkgTest.SetMarkerSize(1)
    hSigTest.SetMarkerColor(ROOT.kBlack)
    hBkgTest.SetMarkerColor(ROOT.kBlue)
    hSigTrain.SetStats(0)
    hBkgTrain.SetStats(0)

    hSigTrain.Scale(1./hSigTrain.Integral())
    hBkgTrain.Scale(1./hBkgTrain.Integral())
    hSigTest.Scale(1./hSigTest.Integral())
    hBkgTest.Scale(1./hBkgTest.Integral())
    yMax = max(hSigTrain.GetMaximum(), hBkgTrain.GetMaximum())
    hSigTrain.GetYaxis().SetRangeUser(0., yMax*1.6)
    hSigTrain.SetTitle("Gradient Boosting Classifier")
    hSigTrain.GetXaxis().SetTitle("score")
    hSigTrain.GetYaxis().SetTitle("events")
    latex = ROOT.TLatex()
    
    c = ROOT.TCanvas()
    c.cd()
    hSigTrain.Draw("hist")
    hBkgTrain.Draw("hist&same")
    hSigTest.Draw("p&same")
    hBkgTest.Draw("p&same")
    latex.DrawLatexNDC(0.6, 0.83, f"n_estimator = {n_estimator}")
    latex.DrawLatexNDC(0.6, 0.78, "max_depth = 3")
    latex.DrawLatexNDC(0.2, 0.85, f"mass window = {max_window}"+"#sigma_{A}")
    latex.DrawLatexNDC(0.2, 0.8, f"ks score (sig) = {ksProbSig}")
    latex.DrawLatexNDC(0.2, 0.75, f"ks score (bkg) = {ksProbBkg}")
    c.SaveAs(f"{outPlotDir}/finalScore.png")

    #### save the classifier
    print("@@@@ saving the classifier...")
    joblib.dump(clf, f"{outPlotDir}/../classifier.pkl")

    #### optimization
    print("@@@@ start optimizing the significance...")
    hSig = ROOT.TH1D("hSig", "", 100, 0., 1.)
    hBkg = ROOT.TH1D("hBkg", "", 100, 0., 1.)
    y_pred = clf.predict_proba(X)
    for score, weight, label in zip(y_pred, weights, y):
        if label == 0: hBkg.Fill(score[1], weight)
        else: hSig.Fill(score[1], weight)
    hSig.Scale(1./sigScaleFactor)

    nBins = hSig.GetNbinsX()
    nSig = hSig.Integral(0, nBins+1)
    nBkg = hBkg.Integral(0, nBins+1)
    initMetric = sqrt(2*((nSig+nBkg)*log(1+nSig/nBkg)-nSig))
    graph = ROOT.TGraph()
    bestCut = 0
    bestMetric = initMetric
    for bin in range(15, nBins-15):
        nSig = hSig.Integral(bin, nBins+1)
        nBkg = hBkg.Integral(bin, nBins+1)
        try:
            metric = sqrt(2*((nSig+nBkg)*log(1+nSig/nBkg)-nSig))
            graph.AddPoint(bin, metric)
        except:
            print(bin, nSig, nBkg)
            continue
        if metric > bestMetric:
            bestCut = bin
            bestMetric = metric
    bestCut = hSig.GetXaxis().GetBinLowEdge(bestCut)
    improvement = (bestMetric-initMetric) / initMetric
    print(f"@@@@ initMetric = {initMetric:.3f}")
    print(f"@@@@ bestMetric = {bestMetric:.3f}")
    print(f"@@@@ improvement = {improvement*100:.2f}%")
    print(f"@@@@ best cut = {bestCut:.2f}")
    graph.SetLineColor(ROOT.kBlack)
    graph.SetLineWidth(2)
    graph.GetXaxis().SetTitle("score")
    graph.GetYaxis().SetTitle("test statistic")
    latex = ROOT.TLatex()
    c = ROOT.TCanvas()
    c.cd()
    graph.Draw()
    latex.DrawLatexNDC(0.15, 0.83, f"best cut = {bestCut:.2f}")
    latex.DrawLatexNDC(0.15, 0.78, f"initMetric = {initMetric:.3f}")
    latex.DrawLatexNDC(0.15, 0.73, f"bestMetric = {bestMetric:.3f}")
    latex.DrawLatexNDC(0.15, 0.68, f"improved {improvement*100:.2f}%")
    c.SaveAs(f"{outPlotDir}/metric.png")
    return True
    
if __name__ == "__main__":
    for max_window in [5, 5.1, 5.2, 5.3,  5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6., 6.1, 6.2, 6.3, 6.4, 6.5]:
        for n_estimator in [50, 45, 40, 35, 30, 25, 20]:
            if train(max_window, n_estimator):
                exit(0)
