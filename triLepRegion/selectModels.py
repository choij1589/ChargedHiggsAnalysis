import os
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
MASSPOINTs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
              "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA_95",
              "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
              "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]
BACKGROUNDs = ["TTLL_powheg", "VV"]
NHIDDEN = 128
OPTIMIZERs = ["RMSprop", "Adam"]
INITIAL_LRs = [0.001, 0.002, 0.005, 0.01, 0.05]
SCHEDULERs = ["ExponentialLR", "StepLR", "CyclicLR"]
NBATCH = 1024

max_size = -1
split1, split2 = 150000, 200000

# helper functions


def checkKSTest(sig, bkg, optimizer, initial_lr, scheduler):
    file_path = f"{os.environ['WORKDIR']}/triLepRegion/output/ROOT/All/{sig}_vs_{bkg}/ParticleNet_nhidden-{NHIDDEN}_{optimizer}_initial_lr-{str(initial_lr).replace('.', 'p')}_{scheduler}_nbatch-{NBATCH}.root"
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
    dataframe = {}
    dataframe["classifier"] = []
    dataframe["optim"] = []
    dataframe["initial_lr"] = []
    dataframe["scheduler"] = []
    for BACKGROUND in BACKGROUNDs:
        print(f"@@@@ Loading dataset for {BACKGROUND}...")
        is_prompt = True if BACKGROUND == "VV" else False
        f_bkg = TFile.Open(
            f"{os.environ['WORKDIR']}/SelectorOutput/Selector_{BACKGROUND}.root")
        bkg_datalist = rtfile_to_datalist(
            f_bkg, channel='3Mu', is_signal=False, is_prompt=is_prompt, max_size=max_size)
        f_bkg.Close()
        bkg_datalist = shuffle(bkg_datalist, random_state=953)[:200000]

        for MASSPOINT in MASSPOINTs:
            print(f"@@@@ Loading dataset for {MASSPOINT}...")
            f_sig = TFile.Open(
                f"{os.environ['WORKDIR']}/SelectorOutput/Selector_TTToHcToWAToMuMu_{MASSPOINT}.root")
            sig_datalist = rtfile_to_datalist(
                f_sig, channel='3Mu', is_signal=True, is_prompt=True, max_size=max_size)
            f_sig.Close()
            sig_datalist = shuffle(sig_datalist, random_state=953)[:200000]

            datalist = shuffle(sig_datalist+bkg_datalist, random_state=953)

            # train / valid / test split
            train_dataset = MyDataset(datalist[:split1])
            val_dataset = MyDataset(datalist[split1:split2])
            test_dataset = MyDataset(datalist[split2:])

            train_loader = DataLoader(
                train_dataset, batch_size=1024, shuffle=False, pin_memory=True)
            val_loader = DataLoader(
                val_dataset, batch_size=1024, shuffle=False, pin_memory=True)
            test_loader = DataLoader(
                test_dataset, batch_size=1024, shuffle=False, pin_memory=True)

            print(f"@@@@ Start model selection...")
            models = {}
            for optim, initial_lr, scheduler in product(OPTIMIZERs, INITIAL_LRs, SCHEDULERs):
                ksprob = checkKSTest(MASSPOINT, BACKGROUND,
                                     optim, initial_lr, scheduler)

                if ksprob < 0.3:
                    continue

                tpr, fpr, auc = checkAUC(
                    MASSPOINT, BACKGROUND, train_loader, val_loader, test_loader, optim, initial_lr, scheduler)
                passAUC = abs(auc['valid'] - auc['test'])/auc['test'] < 0.01
                if not passAUC:
                    continue

                models[f'{optim}_{initial_lr}_{scheduler}'] = auc['test']

            assert models
            models = dict(
                sorted(models.items(), key=lambda item: item[1], reverse=True))
            final_model = list(models.keys())[0]
            print(
                f"@@@@ Final model for {MASSPOINT} vs {BACKGROUND}: {final_model}")
            final_model = final_model.split("_")

            # update dataframe
            dataframe["classifier"].append(f"{MASSPOINT}_vs_{BACKGROUND}")
            dataframe["background"].append(BACKGROUND)
            dataframe["optim"].append(final_model[0])
            dataframe["initial_lr"].append(final_model[1])
            dataframe["scheduler"].append(final_model[2])

    dataframe = pd.DataFrame(dataframe)
    dataframe.to_csv(f"{os.environ['WORKDIR']}/MetaInfo/final_models.csv")
