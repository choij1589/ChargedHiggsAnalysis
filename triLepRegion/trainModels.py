import os, sys
sys.path.insert(0, os.environ['WORKDIR'])
import argparse
#import warnings; warnings.filterwarnings("ignore")

from sklearn.utils          import shuffle
from ROOT                   import TFile

import torch
from torch_geometric.loader import DataLoader

from libPython.Preprocessor import MyDataset
from libPython.Preprocessor import rtfile_to_datalist
from libPython.HistTools    import HistogramWriter
from libPython.MLTools      import SummaryWriter
from libPython.MLTools      import GCN, GNN, ParticleNet
from libPython.MLTools      import EarlyStopping
from libPython.MLTools      import predict, prepare_roc, plot_roc

#### Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--signal", "-s", required=True, type=str, help="signal sample")
parser.add_argument("--background", "-b", required=True, type=str, help="background sample")
parser.add_argument("--model", "-m", default="ParticleNet", type=str, help="model")
parser.add_argument("--hidden_layers", "-l", default=128, type=int, help="the number of hidden layers")
parser.add_argument("--optimizer", "-z", default="Adam", type=str, help="optimizer")
parser.add_argument("--initial_lr", "-i", default=0.15, type=float, help="initial learning rate")
parser.add_argument("--batch_size", "-n", default=1024, type=int, help="batch size")
parser.add_argument("--scheduler", "-c", default="ExponentialLR", type=str, help="learning rate scheducler")
parser.add_argument("--era", "-e", default="All", type=str, help="Era")
parser.add_argument("--pilot", "-p", action="store_true", default=False, help="pilot run")
args = parser.parse_args()

signal_list = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
               "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
               "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
               "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
background_list = ["TTLL_powheg", "VV"]

if not args.signal in signal_list:
    print(f"Wrong signal model {args.signal}")
    exit(1)
if not args.background in background_list:
    print(f"Wrong background model {args.background}")
    exit(1)
if not args.era in ["All", "2016preVFP", "2016postVFP", "2017", "2018"]:
    print(f"Wrong era {args.era}")
    exit(1)

#### pilot mode
max_size = -1 if not args.pilot else 5000
epochs = 300 if not args.pilot else 10

#### Load dataset
print("@@@@ Loading datasets...")
if args.era == "All":
    f_sig = TFile.Open(f"{os.environ['WORKDIR']}/SelectorOutput/Selector_TTToHcToWAToMuMu_{args.signal}.root")
    f_bkg = TFile.Open(f"{os.environ['WORKDIR']}/SelectorOutput/Selector_{args.background}.root")
else:
    f_sig = TFile.Open(f"{os.environ['WORKDIR']}/SelectorOutput/{args.era}/Skim3Mu__/Selector_TTToHcToWAToMuMu_{args.signal}.root")
    f_bkg = TFile.Open(f"{os.environ['WORKDIR']}/SelectorOutput/{args.era}/Skim3Mu__/Selector_{args.background}.root")

is_prompt = True if args.background == "VV" else False
sig_datalist = rtfile_to_datalist(f_sig, 
                                  channel="3Mu", 
                                  is_signal=True, 
                                  is_prompt=True, 
                                  max_size=max_size)
f_sig.Close()
bkg_datalist = rtfile_to_datalist(f_bkg, 
                                  channel="3Mu", 
                                  is_signal=False, 
                                  is_prompt=is_prompt, 
                                  max_size=max_size)
f_bkg.Close()
sig_datalist = shuffle(sig_datalist, random_state=953)[:200000]
bkg_datalist = shuffle(bkg_datalist, random_state=953)[:200000]
datalist = shuffle(sig_datalist+bkg_datalist, random_state=953)

train_dataset = MyDataset(datalist[:int(200000*2*0.4)])
val_dataset = MyDataset(datalist[int(200000*2*0.4):int(200000*2*0.5)])
test_dataset = MyDataset(datalist[int(200000*2*0.5):])

train_loader = DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)
val_loader = DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=4)
test_loader = DataLoader(
        test_dataset, batch_size=args.batch_size, shuffle=False, num_workers=4)
num_features, num_classes = train_dataset[0].num_node_features, train_dataset.num_classes

#### GPU settings
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"@@@@ Using device {DEVICE}...")
if DEVICE == "cuda":
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.enabled = True

#### Helper functions
def train(model, criterion, loader, optimizer, scheduler):
    model.train()

    for data in loader:
        out = model(data.x.to(DEVICE), data.edge_index.to(DEVICE), data.batch.to(DEVICE))
        loss = criterion(out, data.y.to(DEVICE))
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    scheduler.step()

def test(model, criterion, loader):
    model.eval()

    loss = 0.
    correct = 0.
    for data in loader:
        out = model(data.x.to(DEVICE), data.edge_index.to(DEVICE), data.batch.to(DEVICE))
        pred = out.argmax(dim=1)
        answer = data.y.to(DEVICE)
        loss += float(criterion(out, answer).sum())
        correct += int((pred == answer).sum())
    loss /= len(loader.dataset)
    correct /= len(loader.dataset)
    return (loss, correct)

#### Hyperparameter settings
print(f"@@@@ Using model {args.model}...")
if args.model == "GCN":
    model = GCN(num_features, num_classes, args.hidden_layers).to(DEVICE)
elif args.model == "GNN":
    model = GNN(num_features, num_classes, args.hidden_layers).to(DEVICE)
elif args.model == "ParticleNet":
    model = ParticleNet(num_features, num_classes, args.hidden_layers).to(DEVICE)
else:
    print(f"[trainModels] Wrong model name {args.model}")
    exit(1)

print(f"@@@@ Using optimizer {args.optimizer}...")
if args.optimizer == "RMSprop":
    optimizer = torch.optim.RMSprop(model.parameters(), lr=args.initial_lr, momentum=0.9)
elif args.optimizer == "AdamW":
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.initial_lr)
elif args.optimizer == "Adam":
    optimizer = torch.optim.Adam(model.parameters(), lr=args.initial_lr)
elif args.optimizer == "Adadelta":
    optimizer = torch.optim.Adam(model.parameters(), lr=args.initial_lr)
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
            optimizer, base_lr=0.001, max_lr=0.2, step_size_up=3, step_size_down=5, 
            gamma=0.95, mode='exp_range', cycle_momentum=cycle_momentum)
else:
    print(f"[trainModels] Wrong scheduler name {args.scheduler}")
    exit(1)


if __name__ == "__main__":
    model_name = f"{args.model}_nhidden-{args.hidden_layers}_{args.optimizer}_initial_lr-{str(args.initial_lr).replace('.', 'p')}_{args.scheduler}_nbatch-{args.batch_size}"
    checkpoint_path = f"{os.environ['WORKDIR']}/.models/{args.era}/{args.signal}_vs_{args.background}/{model_name}.pt"
    writer_name = f"writer_{model_name}"
    summary_path = f"{os.environ['WORKDIR']}/triLepRegion/output/plots/{args.era}/{args.signal}_vs_{args.background}/training-{model_name}.png"
    roc_path = f"{os.environ['WORKDIR']}/triLepRegion/output/plots/{args.era}/{args.signal}_vs_{args.background}/roc-{model_name}.png"
    outfile_path = f"{os.environ['WORKDIR']}/triLepRegion/output/ROOT/{args.era}/{args.signal}_vs_{args.background}/{model_name}.root"

    criterion = torch.nn.CrossEntropyLoss()
    early_stopper = EarlyStopping(patience=8, path=checkpoint_path)
    s_writer = SummaryWriter(name=writer_name)
    h_writer = HistogramWriter(outfile=outfile_path)
    print(f"@@@@ Start training {model_name}...")
    for epoch in range(epochs):
        train(model, criterion, train_loader, optimizer, scheduler)
        train_loss, train_acc = test(model, criterion, train_loader)
        val_loss, val_acc = test(model, criterion, val_loader)
        s_writer.add_scalar("loss/train", train_loss)
        s_writer.add_scalar("loss/validation", val_loss)
        s_writer.add_scalar("accuracy/train", train_acc)
        s_writer.add_scalar("accuracy/validation", val_acc)
        print(f"[EPOCH {epoch}]\tTrain Acc: {train_acc:.4f}\tTrain Loss: {train_loss:.4f}")
        print(f"[EPOCH {epoch}]\tVlaid Acc: {val_acc:.4f}\tValid Loss: {val_loss:.4f}\n")
        early_stopper.update(val_loss, model)
        if early_stopper.early_stop:
            print(f"Early stopping in epoch {epoch}")
            break
    
    print(f"@@@@ Saving final model...")
    torch.save(model.state_dict(), checkpoint_path)
    
    print(f"@@@@ Visualizing results....")
    # train / validation loss, accuracy
    s_writer.visualize_training(summary_path)
    # ROC curve
    model.to("cpu")
    tpr = {}; fpr = {}; auc = {}
    answers, predictions = predict(model, train_loader)
    for ans, pred in zip(answers, predictions):
        if ans == 1:
            h_writer.fill_hist("train/signal/score", pred, 1., 100, 0., 1.)
        else:
            h_writer.fill_hist("train/background/score", pred, 1., 100, 0., 1.)
    tpr['train'], fpr['train'], auc['train'] = prepare_roc(answers, predictions)
    answers, predictions = predict(model, val_loader)
    for ans, pred in zip(answers, predictions):
        if ans == 1:
            h_writer.fill_hist("validation/signal/score", pred, 1., 100, 0., 1.)
        else:
            h_writer.fill_hist("validation/background/score", pred, 1., 100, 0., 1.)
    tpr['valid'], fpr['valid'], auc['valid'] = prepare_roc(answers, predictions)
    answers, predictions = predict(model, test_loader)
    for ans, pred in zip(answers, predictions):
        if ans == 1:
            h_writer.fill_hist("test/signal/score", pred, 1., 100, 0., 1.)
        else:
            h_writer.fill_hist("test/background/score", pred, 1., 100, 0., 1.)
    tpr['test'], fpr['test'], auc['test'] = prepare_roc(answers, predictions)
    plot_roc(tpr, fpr, auc, roc_path)
    h_writer.close()
