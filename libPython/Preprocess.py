import numpy as np
import torch
from torch.utils.data import Dataset
from torch_geometric.data import Data, InMemoryDataset
from ROOT import TLorentzVector
from DataFormat import Muon, Electron, Jet, Particle

def getMuons(evt):
    muons = []
    muons_zip = zip(evt.MuonPtColl,
                    evt.MuonEtaColl,
                    evt.MuonPhiColl,
                    evt.MuonMassColl,
                    evt.MuonChargeColl)
    for pt, eta, phi, mass, charge in muons_zip:
        thisMuon = Muon(pt, eta, phi, mass)
        thisMuon.SetCharge(charge)
        muons.append(thisMuon)
    return muons

def getElectrons(evt):
    electrons = []
    electrons_zip = zip(evt.ElectronPtColl,
                        evt.ElectronEtaColl,
                        evt.ElectronPhiColl,
                        evt.ElectronMassColl,
                        evt.ElectronChargeColl)
    for pt, eta, phi, mass, charge in electrons_zip:
        thisElectron = Electron(pt, eta, phi, mass)
        thisElectron.SetCharge(charge)
        electrons.append(thisElectron)
    return electrons

def getJets(evt):
    jets = []
    jets_zip = zip(evt.JetPtColl,
                   evt.JetEtaColl,
                   evt.JetPhiColl,
                   evt.JetMassColl,
                   evt.JetChargeColl,
                   evt.JetBtagScoreColl,
                   evt.JetIsBtaggedColl)
    for pt, eta, phi, mass, charge, btagScore, isBtagged in jets_zip:
        thisJet = Jet(pt, eta, phi, mass)
        thisJet.SetCharge(charge)
        thisJet.SetBtagScore(btagScore)
        thisJet.SetBtagging(isBtagged)
        jets.append(thisJet)
        
    bjets = list(filter(lambda jet: jet.IsBtagged(), jets))
    return jets, bjets

def getEdgeIndices(nodeList, k=4):
    edgeIndex = []
    edgeAttribute = []
    for i, node in enumerate(nodeList):
        distances = {}
        for j, neigh in enumerate(nodeList):
            # avoid same node
            if node is neigh: continue
            thisPart = TLorentzVector()
            neighPart = TLorentzVector()
            thisPart.SetPxPyPzE(node[0], node[1], node[2], node[3])
            neighPart.SetPxPyPzE(neigh[0], neigh[1], neigh[2], neigh[3])
            distances[j] = thisPart.DeltaR(neighPart)
        distances = dict(sorted(distances.items(), key=lambda item: item[1]))
        for n in list(distances.keys())[:k]:
            edgeIndex.append([i, n])
            edgeAttribute.append([distances[n]])

    return (torch.tensor(edgeIndex, dtype=torch.long), torch.tensor(edgeAttribute, dtype=torch.float))

def evtToGraph(nodeList, y, k=4):
    x = torch.tensor(nodeList, dtype=torch.float)
    edgeIndex, edgeAttribute = getEdgeIndices(nodeList, k=k)
    data = Data(x=x, y=y,
                edge_index=edgeIndex.t().contiguous(),
                edge_attribute=edgeAttribute)
    return data

def rtfileToDataList(rtfile,  isSignal, maxSize=-1):
    dataList = []
    for evt in rtfile.Events:
        muons = getMuons(evt)
        electrons = getElectrons(evt)
        jets, bjets = getJets(evt)
        METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)
        
        # convert event to a graph
        nodeList = []
        objects = muons+electrons+jets; objects.append(METv)
        for obj in objects:
            nodeList.append([obj.E(), obj.Px(), obj.Py(), obj.Pz(),
                             obj.Charge(), obj.BtagScore(),
                             obj.IsMuon(), obj.IsElectron(), obj.IsJet()])
        # NOTE: Each event converted to a directed graph
        # for each node, find 4 nearest particles and connect
        data = evtToGraph(nodeList, y=int(isSignal))
        dataList.append(data)
        
        if len(dataList) == maxSize: break
    print(f"@@@@ no. of dataList ends with {len(dataList)}")
    
    return dataList

def rtfileToDataListV2(rtfile, isSignal, maxSize=-1): 
    dataList = []
    for evt in rtfile.Events:
        muons = getMuons(evt)
        electrons = getElectrons(evt)
        jets, bjets = getJets(evt)
        METv = Particle(evt.METvPt, 0., evt.METvPhi, 0.)

        # convert event to a graph
        nodeList = []
        objects = muons+electrons+jets+[METv]
        for obj in objects:
            nodeList.append([obj.E(), obj.Px(), obj.Py(), obj.Pz(),
                             obj.Charge(), obj.BtagScore(),
                             obj.IsMuon(), obj.IsElectron(), obj.IsJet()])
        # NOTE: Each event converted to a directed graph
        # for each node, find 4 nearest particles and connect
        data = evtToGraph(nodeList, y=int(isSignal))
        # make MTs
        if len(muons) == 3:
            MT1 = muons[0].MT(METv)
            MT2 = muons[1].MT(METv)
            MT3 = muons[2].MT(METv)
            data.graphInput = torch.tensor([[len(jets), len(bjets), evt.METvPt, MT1, MT2, MT3]], dtype=torch.float)
        elif len(electrons) == 1 and  len(muons) == 2:
            MT1 = electrons[0].MT(METv)
            MT2 = muons[0].MT(METv)
            MT3 = muons[1].MT(METv)
            data.graphInput = torch.tensor([[len(jets), len(bjets), evt.METvPt, MT1, MT2, MT3]], dtype=torch.float)
        else:
            print(f"Wrong size of muons {len(muons)} and electrons {len(electrons)}")
            raise(ValueError)
        dataList.append(data)

        if len(dataList) == maxSize: break
    print(f"@@@@ no. of dataList ends with {len(dataList)}")

    return dataList

class ArrayDataset(Dataset):
    def __init__(self, sample):
        super(ArrayDataset, self).__init__()
        self.features = sample.iloc[:, :-1].to_numpy()
        self.labels = sample.iloc[:, -1:].to_numpy()

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        X = torch.FloatTensor(self.features[idx])
        y = torch.LongTensor(self.labels[idx])
        return (X, y)
    

class GraphDataset(InMemoryDataset):
    def __init__(self, data_list):
        super(GraphDataset, self).__init__("./tmp/data")
        self.data_list = data_list
        self.data, self.slices = self.collate(data_list)
