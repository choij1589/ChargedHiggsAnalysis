import os
import sys
sys.path.insert(0, os.environ['WORKDIR'])
import pandas as pd
import torch
from libPython.Preprocessor import evt_to_graph
from libPython.MLTools import ParticleNet

class FileManager():
    def __init__(self, era):
        self.era = era

def predict_proba(model, x, edge_index):
    model.eval()
    with torch.no_grad():
        out = model(x, edge_index)
        proba = out.numpy()[0][1]
    return proba

class MVAManager():
    def __init__(self):
        self.models = {}

        # read from $WORKDIR/MetaInfo/models.csv file
        csv = pd.read_csv(f"{os.environ['WORKDIR']}/MetaInfo/models.csv")
        csv.set_index(['signal', 'background'], inplace=True)
        for signal, background in csv.index:
            idx = (signal, background)
            # model path
            optim = csv.loc[idx, "optim"]
            initial_lr = csv.loc[idx, 'initial_lr']
            scheduler = csv.loc[idx, 'scheduler']

            model_path = f"{os.environ['WORKDIR']}/.models/All/{signal}_vs_{background}/ParticleNet_nhidden-128_{optim}_initial_lr-{str(initial_lr).replace('.', 'p')}_{scheduler}_nbatch-1024.pt"
            
            self.models[f"{signal}vs{background}"] = ParticleNet(
                    num_features=9, num_classes=2, hidden_channels=128)
            self.models[f"{signal}vs{background}"].load_state_dict(
                    torch.load(model_path, map_location=torch.device('cpu')))
            #except:
            #    print(f"[Management::MVAManager] Failed to load the classifier for {signal}vs{background}")
                # failed to load model, clear the content
            #    self.models.pop(f"{signal}vs{background}")
        del csv

    def getScores(self, objects):
        scores = {}
        # first make objects to graph
        node_list = []
        for object in objects:
            node_list.append([object.Pt(),
                              object.Eta(),
                              object.Phi(),
                              object.M(),
                              object.Charge(),
                              object.IsMuon(),
                              object.IsElectron(),
                              object.IsJet(),
                              object.BtagScore()])
        # the function don't need to know it's actual answer, so just set y=1
        data = evt_to_graph(node_list, y=1, k=3)

        # now fill the scores
        for key, model in self.models.items():
            scores[key] = predict_proba(model, data.x, data.edge_index)
        return scores
