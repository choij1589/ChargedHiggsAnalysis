import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch

from array import array
from sklearn.utils import shuffle
from sklearn import metrics
from torch.utils.data import DataLoader
from ROOT import TFile, TTree, TH1D
from Preprocess import ArrayDataset
from Models import SNN

parser = argparse.ArgumentParser()
parser.add_argument("--channel", type=str, required=True, help="channel")
parser.add_argument("--signal", type=str, required=True, help="signal")
parser.add_argument("--background", type=str, required=True, help="background")
args = parser.parse_args()

WORKDIR = os.environ['WORKDIR']
CHANNEL = args.channel
SIG = args.signal
BKG = args.background

def getChromosomes(SIG, BKG, top=10):
    BASEDIR = f"{WORKDIR}/DenseNeuralNet/{CHANNEL}/{SIG}_vs_{BKG}" 
    chromosomes = {}
    for i in range(5):
        csv = pd.read_csv(f"{BASEDIR}/CSV/GAOptimGen{i}.csv").transpose()
        for idx in range(18):
            key = eval(csv.loc[str(idx), 'chromosome'])
            if key in chromosomes.keys(): continue
            chromosomes[key] = float(csv.loc[str(idx), 'fitness'])
            
    #### sort chromosomes
    sortedChromosomes = dict(sorted(chromosomes.items(), key=lambda x: x[1])[:top])
    
    return sortedChromosomes

def getKSprob(tree, idx):
    hSigTrain = TH1D("hSigTrain", "", 10000, 0., 1.)
    hBkgTrain = TH1D("hBkgTrain", "", 10000, 0., 1.)
    hSigTest = TH1D("hSigTest", "", 10000, 0., 1.)
    hBkgTest = TH1D("hBkgTest", "", 10000, 0., 1.)

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if trainMask[0]: 
            if signalMask[0]: hSigTrain.Fill(scores[f"model{idx}"][0])
            else:             hBkgTrain.Fill(scores[f"model{idx}"][0])
        if testMask[0]:  
            if signalMask[0]: hSigTest.Fill(scores[f"model{idx}"][0])
            else:             hBkgTest.Fill(scores[f"model{idx}"][0])

    ksProbSig = hSigTrain.KolmogorovTest(hSigTest, option="X")
    ksProbBkg = hBkgTrain.KolmogorovTest(hBkgTest, option="X")
    del hSigTrain, hBkgTrain, hSigTest, hBkgTest

    return ksProbSig, ksProbBkg

def getAUC(tree, idx, whichset):
    predictions = []
    answers = []

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if whichset == "train":
            if not trainMask[0]: continue
        elif whichset == "valid":
            if not validMask[0]: continue
        elif whichset == "test":
            if not testMask[0]: continue
        else:
            print(f"Wrong input {whichset}")
            return None

        predictions.append(scores[f"model{idx}"][0])
        answers.append(signalMask[0])

    fpr, tpr, _ = metrics.roc_curve(answers, predictions, pos_label=1)
    auc = metrics.auc(fpr, tpr)
    return auc

def prepareROC(model, loader):
    model.eval()
    predictions = []
    answers = []
    with torch.no_grad():
        for data, label in loader:
            label = label.view(len(label))
            pred = model(data)
            for p in pred: predictions.append(p[1].numpy())
            for a in label: answers.append(a.numpy())
    predictions = np.array(predictions)
    answers = np.array(answers)
    fpr, tpr, _ = metrics.roc_curve(answers, predictions, pos_label=1)
    auc = metrics.auc(fpr, tpr)
    
    return (fpr, tpr, auc)

def plotROC(model, trainLoader, validLoader, testLoader, path):
    plt.figure(figsize=(12, 12))
    plt.title(f"ROC curve")    
    
    fpr, tpr, auc = prepareROC(model, trainLoader)
    plt.plot(tpr, 1.-fpr, 'b--', label=f"train ROC ({auc:.3f})")
    fpr, tpr, auc = prepareROC(model, validLoader)
    plt.plot(tpr, 1.-fpr, 'g--', label=f"valid ROC ({auc:.3f})")
    fpr, tpr, auc = prepareROC(model, testLoader)
    plt.plot(tpr, 1.-fpr, 'r--', label=f"test ROC ({auc:.3f})")
    plt.legend(loc='best')
    plt.xlabel("sig eff.")
    plt.ylabel("bkg rej.")
    plt.savefig(path)
    plt.close()

def plotTrainingStage(idx, path):
    nNodes, optimizer, initLR, scheduler = list(chromosomes.keys())[idx]
    csvPath = f"{WORKDIR}/DenseNeuralNet/{CHANNEL}/{SIG}_vs_{BKG}/CSV/SNN-nNodes{nNodes}_{optimizer}_initLR-{str(initLR).replace('.', 'p')}_{scheduler}.csv"
    record = pd.read_csv(csvPath, index_col=0).transpose()

    trainLoss = list(record.loc['loss/train'])
    validLoss = list(record.loc['loss/valid'])
    trainAcc  = list(record.loc['acc/train'])
    validAcc  = list(record.loc['acc/valid'])

    plt.figure(figsize=(21, 18))
    plt.subplot(2, 1, 1)
    plt.plot(range(1, len(trainLoss)+1), trainLoss, "b--", label="train loss")
    plt.plot(range(1, len(validLoss)+1), validLoss, "r--", label="valid loss")
    plt.legend(loc='best')
    plt.xlabel("epochs")
    plt.ylabel("loss")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(range(1, len(trainAcc)+1), trainAcc, "b--", label="train accuracy")
    plt.plot(range(1, len(validAcc)+1), validAcc, "r--", label="valid accuracy")
    plt.legend(loc='best')
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.grid(True)
    plt.savefig(path)
    plt.close()

#### load datasets
signal = shuffle(pd.read_csv(f"{os.environ['WORKDIR']}/data/DataPreprocess/Combined/{args.channel}__/CSV/{args.signal}.csv", index_col=0), random_state=42)
bkg = shuffle(pd.read_csv(f"{os.environ['WORKDIR']}/data/DataPreprocess/Combined/{args.channel}__/CSV/{args.background}.csv", index_col=0), random_state=42)
signal['label'] = 1
bkg['label'] = 0

sample = shuffle(pd.concat([signal, bkg]), random_state=42)
trainset = ArrayDataset(sample[:int(len(sample)*0.6)])
validset = ArrayDataset(sample[int(len(sample)*0.6):int(len(sample)*0.7)])
testset  = ArrayDataset(sample[int(len(sample)*0.7):])

trainLoader = DataLoader(trainset, batch_size=1024, pin_memory=True, shuffle=True)
validLoader = DataLoader(validset, batch_size=1024, pin_memory=True, shuffle=False)
testLoader  = DataLoader(testset, batch_size=1024, pin_memory=True, shuffle=False)

#### load models
chromosomes = getChromosomes(SIG, BKG)
models =  {}
for idx in range(10):
    nNodes, optimizer, initLR, scheduler = list(chromosomes.keys())[idx]
    modelPath = f"{WORKDIR}/DenseNeuralNet/{CHANNEL}/{SIG}_vs_{BKG}/models/SNN-nNodes{nNodes}_{optimizer}_initLR-{str(initLR).replace('.', 'p')}_{scheduler}.pt"
    model = SNN(len(signal.columns)-1, 2, nNodes, 0.4)
    model.load_state_dict(torch.load(modelPath, map_location=torch.device('cpu')))
    
    models[idx] = model
    
#### prepare directories
outputPath = f"{WORKDIR}/DenseNeuralNet/{CHANNEL}/{SIG}_vs_{BKG}/results/temp.png"
if not os.path.exists(os.path.dirname(outputPath)): os.makedirs(os.path.dirname(outputPath))

#### save score distributions
f = TFile(f"{os.path.dirname(outputPath)}/scores.root", "recreate")
tree = TTree("Events", "")

# initiate branches
scoreBranch = {}
trainMask  = array('B', [False]); tree.Branch("trainMask", trainMask, "trainMask/O")
validMask  = array('B', [False]); tree.Branch("validMask", validMask, "validMask/O")
testMask   = array('B', [False]); tree.Branch("testMask", testMask, "testMask/O")
signalMask = array('B', [False]); tree.Branch("signalMask", signalMask, "signalMask/O")

for idx in models.keys():
    scoreBranch[f"score-model{idx}"] = array('f', [0.])
    tree.Branch(f"score-model{idx}", scoreBranch[f"score-model{idx}"], f"score-model{idx}/F")

# start filling
print("@@@@ Filling trainset...")
trainMask[0] = True; validMask[0] = False; testMask[0] = False
for data, label in trainLoader:
    label = label.view(len(label))
    scoreBatch = {}
    for idx in models.keys():
        scoreBatch[idx] = []
    
    # fill scores 
    with torch.no_grad():
        for idx, model in models.items():
            model.eval()
            scores = model(data)
            for score in scores: 
                scoreBatch[idx].append(score[1].numpy())
    
    # fill events
    for i in range(len(scoreBatch[0])):
        for idx in models.keys():
            scoreBranch[f"score-model{idx}"][0] = scoreBatch[idx][i]
        signalMask[0] = True if label[i] == 1 else False
        tree.Fill()
        
print("@@@@ Filling validset...")
trainMask[0] = False; validMask[0] = True; testMask[0] = False
for data, label in validLoader:
    label = label.view(len(label))
    scoreBatch = {}
    for idx in models.keys():
        scoreBatch[idx] = []
    
    # fill scores 
    with torch.no_grad():
        for idx, model in models.items():
            model.eval()
            scores = model(data)
            for score in scores: 
                scoreBatch[idx].append(score[1].numpy())
    
    # fill events
    for i in range(len(scoreBatch[0])):
        for idx in models.keys():
            scoreBranch[f"score-model{idx}"][0] = scoreBatch[idx][i]
        signalMask[0] = True if label[i] == 1 else False
        tree.Fill()
        
print("@@@@ Filling testset...")
trainMask[0] = False; validMask[0] = False; testMask[0] = True
for data, label in testLoader:
    label = label.view(len(label))
    scoreBatch = {}
    for idx in models.keys():
        scoreBatch[idx] = []
    
    # fill scores 
    with torch.no_grad():
        for idx, model in models.items():
            model.eval()
            scores = model(data)
            for score in scores: 
                scoreBatch[idx].append(score[1].numpy())
    
    # fill events
    for i in range(len(scoreBatch[0])):
        for idx in models.keys():
            scoreBranch[f"score-model{idx}"][0] = scoreBatch[idx][i]
        signalMask[0] = True if label[i] == 1 else False
        tree.Fill()
f.cd()
tree.Write()
f.Close()

#### load tree and start estimation
f = TFile.Open(f"{WORKDIR}/DenseNeuralNet/{CHANNEL}/{SIG}_vs_{BKG}/results/scores.root")
tree = f.Get("Events")

scores = {}
for idx in range(10):
    scores[f"model{idx}"] = array('f', [0.]); tree.SetBranchAddress(f"score-model{idx}", scores[f"model{idx}"])
trainMask = array("B", [False]); tree.SetBranchAddress(f"trainMask", trainMask)
validMask = array("B", [False]); tree.SetBranchAddress(f"validMask", validMask)
testMask = array("B", [False]); tree.SetBranchAddress(f"testMask", testMask)
signalMask = array("B", [False]); tree.SetBranchAddress(f"signalMask", signalMask)

bestModelIdx = -1
bestAUC = 0.
for idx in range(10):
    ksProbSig, ksProbBkg = getKSprob(tree, idx)
    if not (ksProbSig > 0.1 and ksProbBkg > 0.1): continue

    testAUC = getAUC(tree, idx, "test")
    print(f"model-{idx} with testAUC = {testAUC:.3f}")
    if bestAUC < testAUC:
        bestModelIdx = idx
        bestAUC = testAUC
print(f"best model: model-{bestModelIdx} with test AUC {bestAUC:.3f}")
nNodes, optimizer, initLR, scheduler = list(chromosomes.keys())[bestModelIdx]
trainAUC = getAUC(tree, bestModelIdx, "train")
validAUC = getAUC(tree, bestModelIdx, "valid")
testAUC  = getAUC(tree, bestModelIdx, "test")
ksProbSig, ksProbBkg = getKSprob(tree, bestModelIdx)
f.Close()

#### write selection
selectionInfo = f"{SIG}, {BKG}, {bestModelIdx}, {nNodes}, {optimizer}, {initLR}, {scheduler}, {trainAUC}, {validAUC}, {testAUC}, {ksProbSig}, {ksProbBkg}"
print(f"[evalModels] {SIG}_vs_{BKG} summary: {selectionInfo}")
with open(f"{WORKDIR}/DenseNeuralNet/{CHANNEL}/{SIG}_vs_{BKG}/results/summary.txt", "w") as f:
    f.write(f"{selectionInfo}\n")

#### make plots
print("@@@@ Visualizing...")
for idx, model in models.items():    
    plotROC(model, trainLoader, validLoader, testLoader, f"{os.path.dirname(outputPath)}/ROC-model{idx}.png") 
    plotTrainingStage(idx, f"{os.path.dirname(outputPath)}/training-model{idx}.png") 
