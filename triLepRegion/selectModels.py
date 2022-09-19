import os
import sys; sys.path.insert(0, os.environ['WORKDIR'])
import argparse
from itertools import product

import pandas as pd
import torch
from torch_geometric.loader import DataLoader

from sklearn.utils import shuffle
from ROOT import TFile
from libPython.Preprocessor import MyDataset
from libPython.Preprocessor import rtfile_to_datalist
from libPython.MLTools import ParticleNet
from libPython.MLTools import predict, prepare_roc

# Hyper Parameters
parser = argparse.ArgumentParser()
parser.add_argument("--signal", "-s", type=str, required=True)
parser.add_argument("--background", "-b", type=str, required=True)
args = parser.parse_args()

NHIDDEN = 128
OPTIMIZERs = ["RMSprop", "Adam"]
INITIAL_LRs = [0.001, 0.002, 0.005, 0.008, 0.01]
SCHEDULERs = ["ExponentialLR", "StepLR"]
NBATCH = 1024

max_size = -1
split1, split2 = 150000, 200000


# helper functions
def checkKSTest(sig, bkg, optimizer, initial_lr, scheduler):
    file_path = f"{os.environ['WORKDIR']}/triLepRegion/ROOT/All/{sig}_vs_{bkg}/ParticleNet_nhidden-{NHIDDEN}_{optimizer}_initial_lr-{str(initial_lr).replace('.', 'p')}_{scheduler}_nbatch-{NBATCH}.root"
    resultFile = TFile.Open(file_path)
    train_score = resultFile.Get("train/signal/score")
    train_score.Add(resultFile.Get("train/background/score"))
    valid_score = resultFile.Get("validation/signal/score")
    valid_score.Add(resultFile.Get("validation/background/score"))
    test_score = resultFile.Get("test/signal/score")
    test_score.Add(resultFile.Get("test/background/score"))
    train_score.SetDirectory(0)
    valid_score.SetDirectory(0)
    test_score.SetDirectory(0)
    resultFile.Close()
    
    if train_score.Integral() == 0. or test_score.Integral() == 0:
        return None

    ksprob = train_score.KolmogorovTest(test_score, option='X')
    return ksprob


def checkAUC(sig, bkg, train_loader, val_loader, test_loader, optimizer, initial_lr, scheduler):
    model_path = f"{os.environ['WORKDIR']}/.models/All/{sig}_vs_{bkg}/ParticleNet_nhidden-{NHIDDEN}_{optimizer}_initial_lr-{str(initial_lr).replace('.', 'p')}_{scheduler}_nbatch-{NBATCH}.pt"
    model = ParticleNet(num_features=9, num_classes=2, hidden_channels=NHIDDEN)
    model.load_state_dict(torch.load(
        model_path, map_location=torch.device('cpu')))

    tpr = {}
    fpr = {}
    auc = {}
    answers, predictions = predict(model, train_loader)
    tpr['train'], fpr['train'], auc['train'] = prepare_roc(
        answers, predictions)

    answers, predictions = predict(model, val_loader)
    tpr['valid'], fpr['valid'], auc['valid'] = prepare_roc(
        answers, predictions)

    answers, predictions = predict(model, test_loader)
    tpr['test'], fpr['test'], auc['test'] = prepare_roc(answers, predictions)

    return (tpr, fpr, auc)

if __name__ == "__main__":
    print(f"@@@@ Loading dataset for {args.signal} and {args.background}...")
    is_prompt = True if args.background == "VV" else False
    f_sig = TFile.Open(
                f"{os.environ['WORKDIR']}/SelectorOutput/Selector_TTToHcToWAToMuMu_{args.signal}.root")
    f_bkg = TFile.Open(
                f"{os.environ['WORKDIR']}/SelectorOutput/Selector_{args.background}.root")
    sig_datalist = rtfile_to_datalist(
                f_sig, channel='3Mu', is_signal=True, is_prompt=True, max_size=max_size)
    bkg_datalist = rtfile_to_datalist(
                f_bkg, channel='3Mu', is_signal=False, is_prompt=is_prompt, max_size=max_size)
    f_sig.Close()
    f_bkg.Close()

    sig_datalist = shuffle(sig_datalist, random_state=953)[:200000]
    bkg_datalist = shuffle(bkg_datalist, random_state=953)[:200000]
    datalist = shuffle(sig_datalist+bkg_datalist, random_state=953)

    # train / valid / test split
    train_dataset = MyDataset(datalist[:split1])
    val_dataset = MyDataset(datalist[split1:split2])
    test_dataset = MyDataset(datalist[split2:])

    train_loader = DataLoader(train_dataset, batch_size=1024, shuffle=False, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=1024, shuffle=False, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=1024, shuffle=False, pin_memory=True)

    print(f"@@@@ Start model selection...")
    models = {}
    for optim, initial_lr, scheduler in product(OPTIMIZERs, INITIAL_LRs, SCHEDULERs):
        ksprob = checkKSTest(args.signal, args.background, optim, initial_lr, scheduler)
        if not ksprob or ksprob < 0.2:
            continue

        tpr, fpr, auc = checkAUC(args.signal, args.background, 
                                 train_loader, val_loader, test_loader, 
                                 optim, initial_lr, scheduler)
        passAUC = abs(auc['valid'] - auc['test'])/auc['test'] < 0.01
        if not passAUC:
            continue

        models[f'{optim}_{initial_lr}_{scheduler}'] = auc['test']
    try:
        assert models
        models = dict(sorted(models.items(), key=lambda item: item[1], reverse=True))
        final_model = list(models.keys())[0]
        print(f"@@@@ Final model for {args.signal} vs {args.background}: {final_model}")
        final_model = final_model.split("_")
        optim, initial_lr, scheduler = final_model[0], final_model[1], final_model[2]
    
        ksprob = checkKSTest(args.signal, args.background, optim, initial_lr, scheduler)
        tpr, fpr, auc = checkAUC(args.signal, args.background, 
                                 train_loader, val_loader, test_loader,
                                 optim, initial_lr, scheduler)
    except Exception as e:
        print(e)
        optim = "-"
        initial_lr = "-"
        scheduler = "-"
        ksprob = 0.
        auc = {}
        auc['train'] = 0.
        auc['valid'] = 0.
        auc['test'] = 0.

    f = open(f"{os.environ['WORKDIR']}/MetaInfo/models.csv", "a", encoding='utf-8')
    f.write(f"{args.signal},{args.background},{optim},{initial_lr},{scheduler},")
    f.write(f"{ksprob},{auc['train']},{auc['valid']},{auc['test']}\n") 
    f.close()
    
