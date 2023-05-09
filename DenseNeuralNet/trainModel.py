import os
import argparse

from sklearn.utils import shuffle
import pandas as pd

import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F

from Models import SNN, SNNLite
from Preprocess import ArrayDataset
from MLTools import EarlyStopper, SummaryWriter

#### parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--signal", required=True, type=str, help="signal")
parser.add_argument("--background", required=True, type=str, help="background")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--model", required=True, type=str, help="model type")
parser.add_argument("--optimizer", required=True, type=str, help="optimizer")
parser.add_argument("--initLR", required=True, type=float, help="initial learning rate")
parser.add_argument("--scheduler", required=True, type=str, help="lr scheduler")
parser.add_argument("--device", default="cpu", type=str, help="cpu or cuda")
args = parser.parse_args()

# check arguments
channelList = ["Skim1E2Mu", "Skim3Mu"]
signalList = ["MHc-70", "MHc-100", "MHc-130", "MHc-160",
              "MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
              "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
              "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
              "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
backgroundList = ["nonprompt", "diboson", "ttZ"]
if not args.channel in channelList:
    print(f"[trainModels] Wrong channel {args.channel}")
    exit(1)
if not args.signal in signalList:
    print(f"[trainModels] Wrong signal model {args.signal}")
    exit(1)
if not args.background in backgroundList:
    print(f"[trainModels] Wrong background {args.background}")
    exit(1)
    
WORKDIR = os.environ['WORKDIR']

#### load dataset
signal = shuffle(pd.read_csv(f"{os.environ['WORKDIR']}/data/Combined/{args.channel}__/CSV/{args.signal}.csv", index_col=0), random_state=42)
bkg = shuffle(pd.read_csv(f"{os.environ['WORKDIR']}/data/Combined/{args.channel}__/CSV/{args.background}.csv", index_col=0), random_state=42)
signal['label'] = 1
bkg['label'] = 0

sample = shuffle(pd.concat([signal, bkg]), random_state=42)
trainset = sample[:int(len(sample)*0.6)]
validset = sample[int(len(sample)*0.6):int(len(sample)*0.7)]
testset  = sample[int(len(sample)*0.7):]

trainLoader = DataLoader(ArrayDataset(trainset), batch_size=1024, pin_memory=True, shuffle=True)
validLoader = DataLoader(ArrayDataset(validset), batch_size=1024, pin_memory=True, shuffle=False)
testLoader  = DataLoader(ArrayDataset(testset), batch_size=1024, pin_memory=True, shuffle=False)

#### setup
print(f"@@@@ Using model {args.model}...")
if args.model == "SNN":
    model = SNN(len(signal.columns)-1,  2).to(args.device)
elif args.model == "SNNLite":
    model = SNNLite(len(signal.columns)-1, 2).to(args.device)
else:
    print(f"[trainModel] Wrong model name {args.model}")
    exit(1)
#model = torch.compile(model)
print(f"@@@@ Using optimizer {args.optimizer}")
if args.optimizer == "RMSprop":
    optimizer = torch.optim.RMSprop(model.parameters(), lr=args.initLR, momentum=0.9)
elif args.optimizer == "AdamW":
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.initLR)
elif args.optimizer == "Adam":
    optimizer = torch.optim.Adam(model.parameters(), lr=args.initLR)
elif args.optimizer == "Adadelta":
    optimizer = torch.optim.Adadelta(model.parameters(), lr=args.initLR)
elif args.optimizer == "NAdam":
    optimizer = torch.optim.NAdam(model.parameters(), lr=args.initLR)
elif args.optimizer == "RAdam":
    optimizer = torch.optim.RAdam(model.parameters(), lr=args.initLR)
else:
    print(f"[trainModels] Wrong optimizer name {args.optimizer}")
    exit(1)

print(f"@@@@ Using lr scheduler {args.scheduler}...")
if args.scheduler == "StepLR":
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.9)
elif args.scheduler == "ExponentialLR":
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
elif args.scheduler == "CyclicLR":
    cycle_momentum = True if args.optimizer == "RMSprop" else False
    scheduler = torch.optim.lr_scheduler.CyclicLR(
            optimizer,
            base_lr=args.initLR/5., max_lr=args.initLR*2,
            step_size_up=3, step_size_down=5,
            cycle_momentum=cycle_momentum)
else:
    print(f"[trainModels] Wrong scheduler name {args.scheduler}")
    exit(1)

if "cuda" in args.device:
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.enabled = True

def train(model, optimizer, scheduler):
    model.train()

    for data, label in trainLoader:
        data, label = data.to(args.device), label.to(args.device)
        out = model(data)
        loss = F.cross_entropy(out, label.view(len(label)))
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    scheduler.step()

def test(model, loader):
    model.eval()

    loss = 0.
    correct = 0
    with torch.no_grad():
        for data, label in loader:
            data, label = data.to(args.device), label.to(args.device)
            out = model(data)
            pred = out.max(1, keepdim=True)[1]
            loss += F.cross_entropy(out, label.view(len(label)), reduction="sum").item()
            correct += pred.eq(label.view_as(pred)).sum().item()

    loss /= len(loader.dataset)
    correct /= len(loader.dataset)
    
    return (loss, correct)

if __name__ == "__main__":
    modelName = f"{args.model}_{args.optimizer}_initLR-{str(args.initLR).replace('.','p')}_{args.scheduler}"
    print(f"@@@@ Start training...")
    checkptpath = f"{WORKDIR}/DenseNeuralNet/{args.channel}/{args.signal}_vs_{args.background}/models/{modelName}.pt"
    summarypath = f"{WORKDIR}/DenseNeuralNet/{args.channel}/{args.signal}_vs_{args.background}/CSV/{modelName}.csv"
    earlyStopper = EarlyStopper(patience=20, path=checkptpath)
    summaryWriter = SummaryWriter(name=modelName)
    
    for epoch in range(300):
        train(model, optimizer, scheduler)
        trainLoss, trainAcc = test(model, trainLoader)
        validLoss, validAcc = test(model, validLoader)
        summaryWriter.addScalar("loss/train", trainLoss)
        summaryWriter.addScalar("loss/valid", validLoss)
        summaryWriter.addScalar("acc/train", trainAcc)
        summaryWriter.addScalar("acc/valid", validAcc)

        print(f"[EPOCH {epoch}]\tTrain Acc: {trainAcc*100:.2f}\tTrain Loss: {trainLoss:.4e}")
        print(f"[EPOCH {epoch}]\tVlaid Acc: {validAcc*100:.2f}\tValid Loss: {validLoss:.4e}\n")

        panelty = max(0, validLoss-trainLoss)
        earlyStopper.update(validLoss, panelty, model)
        if earlyStopper.earlyStop:
            print(f"Early stopping in epoch {epoch}"); break
    
    summaryWriter.to_csv(summarypath)
