import os
import sys; sys.path.insert(0, os.environ['WORKDIR'])
import argparse

from sklearn.utils          import shuffle
from ROOT                   import TFile

import torch
from torch_geometric.loader import DataLoader

from libPython.Preprocessor import MyDataset
from libPython.Preprocessor import rtfile_to_datalist
from libPython.MLTools      import GCN, GNN, ParticleNet, ParticleNetLite
from libPython.MLTools      import EarlyStopping
from libPython.MLTools      import predict, prepare_roc, plot_roc
from libPython.MLTools      import SummaryWriter

#### Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--signal", required=True, type=str, help="signal sample")
parser.add_argument("--background", required=True, type=str, help="background sample")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--model", required=True, type=str, help="model type")
parser.add_argument("--optimizer", required=True, type=str, help="optimizer")
parser.add_argument("--initLR", required=True, type=float, help="initial learning rate")
parser.add_argument("--scheduler", required=True, type=str, help="lr scheducler")
parser.add_argument("--pilot", action="store_true", default=False, help="pilot run")
parser.add_argument("--device", default="cpu", type=str, help="device to use")
args = parser.parse_args()

# check arguments
signalList = ["MHc-70", "MHc-100", "MHc-130", "MHc-160",
              "MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
              "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
              "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
              "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
backgroundList = ["TTLL_powheg", "ttX"]

if not args.signal in signalList:
    print(f"[trainModels] Wrong signal model {args.signal}")
    exit(1)
if not args.background in backgroundList:
    print(f"[trainModels] Wrong background {args.background}")
    exit(1)

#### Hyperparameter settings
nFeatures = 9
nClasses = 2
print(f"@@@@ Using model {args.model}...")
if args.model == "GCN":
    model = GCN(nFeatures, nClasses).to(args.device)
elif args.model == "GNN":
    model = GNN(nFeatures, nClasses).to(args.device)
elif args.model == "ParticleNet":
    model = ParticleNet(nFeatures, nClasses).to(args.device)
elif args.model == "ParticleNetLite":
    model = ParticleNetLite(nFeatures, nClasses).to(args.device)
else:
    print(f"[trainModels] Wrong model name {args.model}")
    exit(1)

print(f"@@@@ Using optimizer {args.optimizer}...")
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
stopperPatience = 6
if args.scheduler == "StepLR":
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.9)
elif args.scheduler == "ExponentialLR":
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
elif args.scheduler == "CyclicLR":
    cycle_momentum = True if args.optimizer == "RMSprop" else False
    stopperPatience = 10
    scheduler = torch.optim.lr_scheduler.CyclicLR(
            optimizer, 
            base_lr=args.initLR/5., max_lr=args.initLR*2, 
            step_size_up=3, step_size_down=5,
            cycle_momentum=cycle_momentum)
else:
    print(f"[trainModels] Wrong scheduler name {args.scheduler}")
    exit(1)

#### pilot mode
#### It is used in both debugging and finding optimal hyperparameter
if args.pilot:
    maxSize = 50000
    epochs = 30
else:
    maxSize = 100000
    epochs = 200
    if args.channel == "Skim1E2Mu" and args.background == "TTLL_powheg":
        maxSize = 90000

#### Load dataset
rtSig = TFile.Open(f"{os.environ['WORKDIR']}/SelectorOutput/Training/{args.channel}__/Selector_TTToHcToWAToMuMu_{args.signal}.root")
rtBkg = TFile.Open(f"{os.environ['WORKDIR']}/SelectorOutput/Training/{args.channel}__/Selector_{args.background}.root")

isPrompt = False if args.background == "TTLL_powheg" else True
channel = args.channel[4:]
sigDatalist = rtfile_to_datalist(rtSig, channel=channel, is_signal=True, is_prompt=True)
bkgDatalist = rtfile_to_datalist(rtBkg, channel=channel, is_signal=False, is_prompt=isPrompt)
rtSig.Close()
rtBkg.Close()

sigDatalist = shuffle(sigDatalist, random_state=42)[:maxSize]
bkgDatalist = shuffle(bkgDatalist, random_state=42)[:maxSize]
datalist = shuffle(sigDatalist+bkgDatalist, random_state=42)

trainDataset = MyDataset(datalist[:int(maxSize*2*0.6)])
validDataset = MyDataset(datalist[int(maxSize*2*0.6):int(maxSize*2*0.7)])
testDataset = MyDataset(datalist[int(maxSize*2*0.7):])

trainLoader = DataLoader(trainDataset, batch_size=1024, shuffle=True, pin_memory=True)
validLoader = DataLoader(validDataset, batch_size=1024, shuffle=False, pin_memory=True)
testLoader = DataLoader(testDataset, batch_size=1024, shuffle=False, pin_memory=True)

#### GPU settings
if "cuda" in args.device:
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.enabled = True

#### helper functions
def train(model, criterion, optimizer, scheduler):
    model.train()

    for data in trainLoader:
        out = model(data.x.to(args.device), data.edge_index.to(args.device), data.batch.to(args.device))
        loss = criterion(out, data.y.to(args.device))
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    scheduler.step()

def test(model, criterion, loader):
    model.eval()

    loss = 0.
    correct = 0.
    for data in loader:
        out = model(data.x.to(args.device), data.edge_index.to(args.device), data.batch.to(args.device))
        pred = out.argmax(dim=1)
        answer = data.y.to(args.device)
        loss += float(criterion(out, answer).sum())
        correct += int((pred == answer).sum())
    loss /= len(loader.dataset)
    correct /= len(loader.dataset)
    return (loss, correct)

if __name__ == "__main__":
    modelName = f"{args.model}_{args.optimizer}_initLR-{str(args.initLR).replace('.', 'p')}_{args.scheduler}"
    if args.pilot:
        checkpointPath = f"{os.environ['WORKDIR']}/triLepRegion/pilot/{args.channel}__/{args.signal}_vs_{args.background}/models/{modelName}.pt"
        logPath = f"{os.environ['WORKDIR']}/triLepRegion/pilot/{args.channel}__/{args.signal}_vs_{args.background}/logs/{modelName}.log"
        summaryPath = f"{os.environ['WORKDIR']}/triLepRegion/pilot/{args.channel}__/{args.signal}_vs_{args.background}/plots/training-{modelName}.png"
        rocPath = f"{os.environ['WORKDIR']}/triLepRegion/pilot/{args.channel}__/{args.signal}_vs_{args.background}/plots/roc-{modelName}.png"
    else:
        checkpointPath = f"{os.environ['WORKDIR']}/triLepRegion/full/{args.channel}__/{args.signal}_vs_{args.background}/models/{modelName}.pt"
        logPath = f"{os.environ['WORKDIR']}/triLepRegion/full/{args.channel}__/{args.signal}_vs_{args.background}/logs/{modelName}.log"
        summaryPath = f"{os.environ['WORKDIR']}/triLepRegion/full/{args.channel}__/{args.signal}_vs_{args.background}/plots/training-{modelName}.png"
        rocPath = f"{os.environ['WORKDIR']}/triLepRegion/full/{args.channel}__/{args.signal}_vs_{args.background}/plots/roc-{modelName}.png"

    criterion = torch.nn.CrossEntropyLoss()
    earlyStopper = EarlyStopping(patience=stopperPatience, path=checkpointPath)
    summaryWriter = SummaryWriter(name=modelName)
    print(f"@@@@ Start training {modelName}...")
    for epoch in range(epochs):
        train(model, criterion, optimizer, scheduler)
        trainLoss, trainAcc = test(model, criterion, trainLoader)
        validLoss, validAcc = test(model, criterion, validLoader)
        summaryWriter.add_scalar("loss/train", trainLoss)
        summaryWriter.add_scalar("loss/valid", validLoss)
        summaryWriter.add_scalar("acc/train", trainAcc)
        summaryWriter.add_scalar("acc/valid", validAcc)
        print(f"[EPOCH {epoch}]\tTrain Acc: {trainAcc:.4f}\tTrain Loss: {trainLoss:.4f}")
        print(f"[EPOCH {epoch}]\tVlaid Acc: {validAcc:.4f}\tValid Loss: {validLoss:.4f}\n")

        # early stopping
        panelty = 1.5*abs(trainLoss - validLoss)
        earlyStopper.update(validLoss, panelty, model)
        if earlyStopper.early_stop:
            print(f"Early stopping in epoch {epoch}")
            break
    
    #print(f"@@@@ Saving final model...")
    #torch.save(model.state_dict(), checkpointPath)

    print(f"@@@@ Visualising results...")
    # train / validation loss, accuraccy
    summaryWriter.store_csv(summaryPath.replace("png", "csv"))
    summaryWriter.visualize_training(summaryPath)
    # ROC curve
    model.to("cpu")
    model.load_state_dict(torch.load(checkpointPath, map_location=torch.device('cpu')))
    tpr = {}
    fpr = {}
    auc = {}
    answers, predictions = predict(model, trainLoader)
    tpr['train'], fpr['train'], auc['train'] = prepare_roc(answers, predictions)
    answers, predictions = predict(model, validLoader)
    tpr['valid'], fpr['valid'], auc['valid'] = prepare_roc(answers, predictions)
    answers, predictions = predict(model, testLoader)
    tpr['test'], fpr['test'], auc['test'] = prepare_roc(answers, predictions)
    plot_roc(tpr, fpr, auc, rocPath)
