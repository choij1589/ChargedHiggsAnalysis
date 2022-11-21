import os, sys; sys.path.insert(0, os.environ['WORKDIR'])
import numpy as np
import torch
from torch_geometric.data import Data, InMemoryDataset
from ROOT import TLorentzVector
from libPython.Selection import pass_baseline, select
from libPython.DataFormat import Particle, get_muons, get_electrons, get_jets

class MyDataset(InMemoryDataset):
    def __init__(self, data_list):
        super(MyDataset, self).__init__("./tmp/data")
        self.data_list = data_list
        self.data, self.slices = self.collate(data_list)


def get_edge_indices(node_list, k):
    edge_index = []
    edge_attribute = []
    for i, node in enumerate(node_list):
        distances = {}
        for j, neighbor in enumerate(node_list):
            # avoid same node
            if node is neighbor:
                continue
            thisPart = TLorentzVector()
            neighborPart = TLorentzVector()
            thisPart.SetPxPyPzE(node[1], node[2], node[3], node[0])
            neighborPart.SetPxPyPzE(neighbor[1], neighbor[2], neighbor[3], neighbor[0])
            distances[j] = thisPart.DeltaR(neighborPart)
        distances = dict(sorted(distances.items(), key=lambda item: item[1]))
        for n in list(distances.keys())[:k]:
            edge_index.append([i, n])
            edge_attribute.append([distances[n]])

    return (torch.tensor(edge_index, dtype=torch.long), torch.tensor(edge_attribute, dtype=torch.float))


def evt_to_graph(node_list, y, k=4):
    x = torch.tensor(node_list, dtype=torch.float)
    edge_index, edge_attribute = get_edge_indices(node_list, k=k)
    data = Data(x=x,
                y=y,
                edge_index=edge_index.t().contiguous(),
                edge_attribute=edge_attribute)
    return data


def rtfile_to_datalist(rtfile, channel, is_signal, is_prompt, max_size=-1):
    data_list = []
    for evt in rtfile.Events:
        muons = get_muons(evt)
        electrons = get_electrons(evt)
        jets, bjets = get_jets(evt)
        METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)

        if not pass_baseline(channel, evt, muons, electrons, idstring="loose", isTraining=True):
            continue

        muons_prompt = list(filter(lambda x: x.LepType() > 0, muons))
        electrons_prompt = list(filter(lambda x: x.LepType() > 0, electrons))
        prompt_leptons = (len(muons) == len(muons_prompt)
                          and len(electrons) == len(electrons_prompt))
        if is_prompt:
            if not prompt_leptons:
                continue
        else:
            if prompt_leptons:
                continue

        # Convert each event to a graph
        node_list = []
        objects = muons+electrons+jets
        objects.append(METv)
        for particle in objects:
            node_list.append([particle.E(),
                              particle.Px(),
                              particle.Py(),
                              particle.Pz(),
                              particle.Charge(),
                              particle.IsMuon(),
                              particle.IsElectron(),
                              particle.IsJet(),
                              particle.BtagScore()]
                             )
        x = torch.tensor(node_list, dtype=torch.float)
        # make edges
        # NOTE: Each event is a directed graph!
        # for each node, find 3 nearest particles and connect them
        edge_index, edge_attribute = get_edge_indices(node_list, k=4)
        data = Data(x=x,
                    y=int(is_signal),
                    edge_index=edge_index.t().contiguous(),
                    edge_attribute=edge_attribute)
        data_list.append(data)

        if len(data_list) == max_size:
            break
    print(f"@@@@ the no. of data_list ends with {len(data_list)}")

    return data_list
