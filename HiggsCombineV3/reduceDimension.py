import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

import pickle
import joblib

import ROOT
ROOT.gROOT.SetBatch(True)

#### parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--channel", required=True, type=str, help="channel")
args = parser.parse_args()

#### helper functions
def getFitSigmaValue(mA):
    with open(f"samples/{args.era}/{args.channel}__/interpolResults.csv") as f:
        line = f.readlines()[2].split(",")
    a0 = float(line[0])
    a1 = float(line[1])
    a2 = float(line[2])
    return a0 + a1*mA + a2*(mA**2)

#### global variables
mA = int(args.signal.split("_")[1].split("-")[1])
sigma = getFitSigmaValue(mA)

outPlotDir = f"results/{args.era}/{args.channel}__GraphNet__/{args.signal}/plots"
os.makedirs(outPlotDir, exist_ok=True)

#### load dataset
col_sig = []
f = ROOT.TFile(f"samples/{args.era}/{args.channel}__GraphNet__/{args.signal}/{args.signal}.root")
tree = f.Get(f"{args.signal}_Central")
for idx, evt in enumerate(tree, start=1):
    condition = (mA - 6*sigma < evt.mass1 < mA + 6*sigma) or (mA - 6*sigma < evt.mass2 < mA + 6*sigma)
    if not condition:
        continue
    col_sig.append([evt.scoreX, evt.scoreY, evt.scoreZ, evt.weight, 1.])
col_sig = np.array(col_sig)

col_VV = []
f = ROOT.TFile(f"samples/{args.era}/{args.channel}__GraphNet__/{args.signal}/diboson.root")
tree = f.Get("diboson_Central")
for idx, evt in enumerate(tree, start=1):
    condition = (mA - 6*sigma < evt.mass1 < mA + 6*sigma) or (mA - 6*sigma < evt.mass2 < mA + 6*sigma)
    if not condition:
        continue
    col_VV.append([evt.scoreX, evt.scoreY, evt.scoreZ, evt.weight, 0.])
col_VV = np.array(col_VV)

col_ttX = []
f = ROOT.TFile(f"samples/{args.era}/{args.channel}__GraphNet__/{args.signal}/ttX.root")
tree = f.Get("ttX_Central")
for idx, evt in enumerate(tree, start=1):
    condition = (mA - 6*sigma < evt.mass1 < mA + 6*sigma) or (mA - 6*sigma < evt.mass2 < mA + 6*sigma)
    if not condition:
        continue
    col_ttX.append([evt.scoreX, evt.scoreY, evt.scoreZ, evt.weight, 0.])
col_ttX = np.array(col_ttX)

col_conv = []
f = ROOT.TFile(f"samples/{args.era}/{args.channel}__GraphNet__/{args.signal}/conversion.root")
tree = f.Get("conversion_Central")
for idx, evt in enumerate(tree, start=1):
    condition = (mA - 6*sigma < evt.mass1 < mA + 6*sigma) or (mA - 6*sigma < evt.mass2 < mA + 6*sigma)
    if not condition:
        continue
    col_conv.append([evt.scoreX, evt.scoreY, evt.scoreZ, evt.weight, 0.])
col_conv = np.array(col_conv)

col_fake = []
f = ROOT.TFile(f"samples/{args.era}/{args.channel}__GraphNet__/{args.signal}/nonprompt.root")
tree = f.Get("nonprompt_Central")
for idx, evt in enumerate(tree, start=1):
    condition = (mA - 6*sigma < evt.mass1 < mA + 6*sigma) or (mA - 6*sigma < evt.mass2 < mA + 6*sigma)
    if not condition:
        continue
    col_fake.append([evt.scoreX, evt.scoreY, evt.scoreZ, evt.weight, 0.])
col_fake = np.array(col_fake)

col_others = []
f = ROOT.TFile(f"samples/{args.era}/{args.channel}__GraphNet__/{args.signal}/others.root")
tree = f.Get("others_Central")
for idx, evt in enumerate(tree, start=1):
    condition = (mA - 6*sigma < evt.mass1 < mA + 7*sigma) or (mA - 6*sigma < evt.mass2 < mA + 6*sigma)
    if not condition:
        continue
    col_others.append([evt.scoreX, evt.scoreY, evt.scoreZ, evt.weight, 0.])
col_others = np.array(col_others)

col_bkg = np.concatenate([col_VV, col_ttX, col_others, col_conv, col_fake], axis=0)

## scale signal so that the total events of signals and backgrounds are the same
hX_sig = ROOT.TH1D("hX_sig", "", 100, 0., 1.)
hY_sig = ROOT.TH1D("hY_sig", "", 100, 0., 1.)
hZ_sig = ROOT.TH1D("hZ_sig", "", 100, 0., 1.)
hX_bkg = ROOT.TH1D("hX_bkg", "", 100, 0., 1.)
hY_bkg = ROOT.TH1D("hY_bkg", "", 100, 0., 1.)
hZ_bkg = ROOT.TH1D("hZ_bkg", "", 100, 0., 1.)

for evt in col_sig:
    scoreX, scoreY, scoreZ, weight = tuple(evt[:4])
    hX_sig.Fill(scoreX, weight)
    hY_sig.Fill(scoreY, weight)
    hZ_sig.Fill(scoreZ, weight)

for evt in col_bkg:
    scoreX, scoreY, scoreZ, weight = tuple(evt[:4])
    hX_bkg.Fill(scoreX, weight)
    hY_bkg.Fill(scoreY, weight)
    hZ_bkg.Fill(scoreZ, weight)

print("@@@@ Scaling signal...")
sigScaleFactor = hX_bkg.Integral() / hX_sig.Integral()
print(f"@@@@ nSig = {hX_sig.Integral():.3f}")
print(f"@@@@ nBkg = {hX_bkg.Integral():.3f}")
print(f"@@@@ scale factor = {sigScaleFactor}")
col_sig[:, 3] = col_sig[:, 3]*sigScaleFactor

print("@@@@ Saving input distributions...")
hX_sig.SetLineColor(ROOT.kBlack)
hX_bkg.SetLineColor(ROOT.kRed)

hX_sig.SetLineWidth(2)
hX_bkg.SetLineWidth(2)
hX_sig.Scale(1./hX_sig.Integral())
hX_bkg.Scale(1./hX_bkg.Integral())

hX_sig.SetStats(0)
hX_sig.SetTitle("scoreX")
hX_sig.GetXaxis().SetTitle("score")
hX_sig.GetYaxis().SetTitle("events")

c = ROOT.TCanvas()
c.SetLogy()
c.cd()
hX_sig.Draw("hist")
hX_bkg.Draw("hist&same")
c.SaveAs(f"{outPlotDir}/scoreX.png")

hY_sig.SetLineColor(ROOT.kBlack)
hY_bkg.SetLineColor(ROOT.kRed)

hY_sig.SetLineWidth(2)
hY_bkg.SetLineWidth(2)
hY_sig.Scale(1./hY_sig.Integral())
hY_bkg.Scale(1./hY_bkg.Integral())

hY_sig.SetStats(0)
hY_sig.SetTitle("scoreY")
hY_sig.GetXaxis().SetTitle("score")
hY_sig.GetYaxis().SetTitle("events")

c = ROOT.TCanvas()
c.SetLogy()
c.cd()
hY_sig.Draw("hist")
hY_bkg.Draw("hist&same")
c.SaveAs(f"{outPlotDir}/scoreY.png")

hZ_sig.SetLineColor(ROOT.kBlack)
hZ_bkg.SetLineColor(ROOT.kRed)

hZ_sig.SetLineWidth(2)
hZ_bkg.SetLineWidth(2)
hZ_sig.Scale(1./hZ_sig.Integral())
hZ_bkg.Scale(1./hZ_bkg.Integral())

hZ_sig.SetStats(0)
hZ_sig.SetTitle("scoreZ")
hZ_sig.GetXaxis().SetTitle("score")
hZ_sig.GetYaxis().SetTitle("events")

c = ROOT.TCanvas()
c.SetLogy()
c.cd()
hZ_sig.Draw("hist")
hZ_bkg.Draw("hist&same")
c.SaveAs(f"{outPlotDir}/scoreZ.png")

#fig = plt.figure()
#ax = fig.add_plot(projection='3d')

#ax.scatter(col_sig[:1500, 0], col_sig[:900, 1], col_sig[:1500, 2], marker="o")
#ax.scatter(col_VV[:500, 0], col_VV[:300, 1], col_VV[:500, 2], marker="v")
#ax.scatter(col_fake[:500, 0], col_fake[:300, 1], col_fake[:500, 2], marker="^")
#ax.scatter(col_ttX[:500, 0], col_ttX[:300, 1], col_ttX[:500, 2], marker="P")
#ax.set_xlabel("scoreX")
#ax.set_ylabel("scoreY")
#ax.set_zlabel("scoreZ")
#ax.legend(loc="best")
#plt.close(fig)
#ax.savefig(f"{outPlotDir}/score3D.png")

#### preprocessing
col_bkg = shuffle(col_bkg, random_state=42)
events = np.concatenate([col_sig, col_bkg], axis=0)
events = shuffle(events, random_state=42)

X, weights, y = events[:, :3], events[:, 3], events[:, 4]
X_train, X_test, y_train, y_test, sw_train, sw_test = train_test_split(X, y, weights, test_size=0.4, random_state=42)

## train GBclassifier
print("@@@@ Start training...")
clf = GradientBoostingClassifier(n_estimators=50, max_depth=3)
clf.fit(X_train, y_train, sample_weight=sw_train)
print("@@@@ feature importance")
print(f"@@@@ scoreX = {clf.feature_importances_[0]}")
print(f"@@@@ scoreY = {clf.feature_importances_[1]}")
print(f"@@@@ scoreZ = {clf.feature_importances_[2]}")


## save the trained results
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

ksProbSig = hSigTrain.KolmogorovTest(hSigTest, option="X")
ksProbBkg = hBkgTrain.KolmogorovTest(hBkgTest, option="X")
ksProbSigText = ROOT.TLatex()
ksProbBkgText = ROOT.TLatex()

print(f"@@@@ ksProbSig = {ksProbSig}")
print(f"@@@@ ksProbBkg = {ksProbBkg}")

hSigTrain.GetYaxis().SetRangeUser(0., 0.15)
hSigTrain.SetTitle("GB classifier score")
hSigTrain.GetXaxis().SetTitle("score")
hSigTrain.GetYaxis().SetTitle("events")

c = ROOT.TCanvas()
#c.SetLogy()
c.cd()
hSigTrain.Draw("hist")
hBkgTrain.Draw("hist&same")
hSigTest.Draw("p&same")
hBkgTest.Draw("p&same")
ksProbSigText.DrawLatexNDC(0.5, 0.8, f"ks score (sig) = {ksProbSig}")
ksProbSigText.DrawLatexNDC(0.5, 0.75, f"ks score (bkg) = {ksProbBkg}")
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

from math import sqrt, log

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
print(f"@@@@ best cut = {bestCut}")

graph.SetLineColor(ROOT.kBlack)
graph.SetLineWidth(2)
graph.GetXaxis().SetTitle("score")
graph.GetYaxis().SetTitle("test statistic")
improvementText = ROOT.TLatex()
bestCutText = ROOT.TLatex()

c = ROOT.TCanvas()
c.cd()
graph.Draw()
bestCutText.DrawLatexNDC(0.15, 0.83, f"best cut = {bestCut}")
improvementText.DrawLatexNDC(0.15, 0.78, f"improved {improvement*100:.2f}%")
c.SaveAs(f"{outPlotDir}/metric.png")
