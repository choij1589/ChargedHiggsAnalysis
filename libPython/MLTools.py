import os
import sys; sys.path.insert(0, os.environ['WORKDIR'])

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn.functional as F
from torch.nn import Sequential, Linear, ReLU, BatchNorm1d
from torch_geometric.nn import global_mean_pool, knn_graph
from torch_geometric.nn import GCNConv, GraphConv
from torch_geometric.nn import GraphNorm
from torch_geometric.nn import MessagePassing
from sklearn import metrics

class GCN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(GCN, self).__init__()
        self.gn0 = GraphNorm(num_features)
        self.conv1 = GCNConv(num_features, 64)
        self.gn1 = GraphNorm(64)
        self.conv2 = GCNConv(64, 64)
        self.gn2 = GraphNorm(64)
        self.conv3 = GCNConv(64, 64)
        self.dense = Linear(64, 64)
        self.output = Linear(64, num_classes)

    def forward(self, x, edge_index, batch=None):
        # Convolution layers
        x = self.gn0(x, batch)
        x = F.relu(self.conv1(x, edge_index))
        x = self.gn1(x, batch)
        x = F.relu(self.conv2(x, edge_index))
        x = self.gn2(x, batch)
        x = F.relu(self.conv3(x, edge_index))

        # readout layers
        x = global_mean_pool(x, batch)

        # dense layers
        x = F.dropout(x, p=0.5, training=self.training)
        x = F.relu(self.dense(x))
        x = self.output(x)

        return F.softmax(x, dim=1)


class GNN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(GNN, self).__init__()
        self.gn0 = GraphNorm(num_features)
        self.conv1 = GraphConv(num_features, 64)
        self.gn1 = GraphNorm(64)
        self.conv2 = GraphConv(64, 64)
        self.gn2 = GraphNorm(64)
        self.conv3 = GraphConv(64, 64)
        self.dense = Linear(64, 64)
        self.output = Linear(64, num_classes)

    def forward(self, x, edge_index, batch=None):
        # Convolution layers
        x = self.gn0(x, batch)
        x = F.relu(self.conv1(x, edge_index))
        x = self.gn1(x, batch)
        x = F.relu(self.conv2(x, edge_index))
        x = self.gn2(x, batch)
        x = F.relu(self.conv3(x, edge_index))

        # readout layers
        x = global_mean_pool(x, batch)

        # dense layers
        x = F.dropout(x, p=0.5, training=self.training)
        x = F.relu(self.dense(x))
        x = self.output(x)

        return F.softmax(x, dim=1)


class EdgeConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr='mean')
        self.mlp = Sequential(
                Linear(2 * in_channels, out_channels), BatchNorm1d(out_channels), ReLU(),
                Linear(out_channels, out_channels), BatchNorm1d(out_channels), ReLU(),
                Linear(out_channels, out_channels), BatchNorm1d(out_channels), ReLU())

    def forward(self, x, edge_index, batch=None):
        return self.propagate(edge_index, x=x, batch=batch)

    def message(self, x_i, x_j):
        tmp = torch.cat([x_i, x_j - x_i], dim=1)
        return self.mlp(tmp)


class DynamicEdgeConv(EdgeConv):
    def __init__(self, in_channels, out_channels, k=4):
        super().__init__(in_channels, out_channels)
        self.shortcut = Sequential(Linear(in_channels, out_channels), BatchNorm1d(out_channels))
        self.k = k

    def forward(self, x, edge_index=None, batch=None):
        if edge_index is None:
            edge_index = knn_graph(
                x, self.k, batch, loop=False, flow=self.flow)
        out = super().forward(x, edge_index, batch=batch)
        out += self.shortcut(x)
        return F.relu(out)


class ParticleNet(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(ParticleNet, self).__init__()
        self.gn0 = GraphNorm(num_features)
        self.conv1 = DynamicEdgeConv(num_features, 64)
        self.gn1 = GraphNorm(64)
        self.conv2 = DynamicEdgeConv(64, 128)
        self.gn2 = GraphNorm(128)
        self.conv3 = DynamicEdgeConv(128, 128)
        self.gn3 = GraphNorm(128)
        self.dense1 = Linear(128, 64)
        self.dense2 = Linear(64, 64)
        self.output = Linear(64, num_classes)

    def forward(self, x, edge_index, batch=None):
        # Convolution layers
        x = self.gn0(x, batch=batch)
        x = self.conv1(x, edge_index, batch=batch)
        x = self.gn1(x, batch=batch)
        x = self.conv2(x, batch=batch)
        x = self.gn2(x, batch=batch)
        x = self.conv3(x, batch=batch)
        x = self.gn3(x, batch=batch)
        # readout layers
        x = global_mean_pool(x, batch=batch)

        # dense layers
        x = F.relu(self.dense1(x))
        x = F.dropout(x, p=0.2)
        x = F.relu(self.dense2(x))
        x = F.dropout(x, p=0.2)
        x = self.output(x)

        return F.softmax(x, dim=1)


class ParticleNetLite(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(ParticleNetLite, self).__init__()
        self.gn0 = GraphNorm(num_features)
        self.conv1 = DynamicEdgeConv(num_features, 32)
        self.gn1 = GraphNorm(32)
        self.conv2 = DynamicEdgeConv(32, 64)
        self.gn2 = GraphNorm(64)
        self.conv3 = DynamicEdgeConv(64, 64)
        self.gn3 = GraphNorm(64)
        self.dense1 = Linear(64, 32)
        self.dense2 = Linear(32, 32)
        self.output = Linear(32, num_classes)

    def forward(self, x, edge_index, batch=None):
        # Convolution layers
        x = self.gn0(x, batch=batch)
        x = self.conv1(x, edge_index, batch=batch)
        x = self.gn1(x, batch=batch)
        x = self.conv2(x, batch=batch)
        x = self.gn2(x, batch=batch)
        x = self.conv3(x, batch=batch)
        x = self.gn3(x, batch=batch)
        # readout layers
        x = global_mean_pool(x, batch=batch)

        # dense layers
        x = F.relu(self.dense1(x))
        x = F.dropout(x, p=0.2)
        x = F.relu(self.dense2(x))
        x = F.dropout(x, p=0.2)
        x = self.output(x)

        return F.softmax(x, dim=1)


class EarlyStopping():
    def __init__(self, patience=7, delta=0, path="./checkpoint.pt"):
        self.patience = patience
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.path = path
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    def update(self, val_loss, panelty,  model):
        score = -(val_loss+panelty)
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score <= self.best_score + self.delta:
            self.counter += 1
            print(
                f"[EarlyStopping counter] {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss


class SummaryWriter():
    def __init__(self, name):
        self.name = name
        self.scalar_dict = {}

    def add_scalar(self, key, value):
        # check whether the list exists
        if not key in self.scalar_dict.keys():
            self.scalar_dict[key] = []
        self.scalar_dict[key].append(value)

    def get_scalar(self, key):
        return np.array(self.scalar_dict[key])

    def store_csv(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        df = pd.DataFrame(self.scalar_dict)
        df.to_csv(path)

    def visualize_training(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        assert "loss/train" in self.scalar_dict.keys()
        assert "loss/valid" in self.scalar_dict.keys()
        assert "acc/train" in self.scalar_dict.keys()
        assert "acc/valid" in self.scalar_dict.keys()

        train_loss = self.get_scalar("loss/train")
        val_loss = self.get_scalar("loss/valid")
        train_acc = self.get_scalar("acc/train")
        val_acc = self.get_scalar("acc/valid")
        epochs = np.arange(1, len(train_loss)+1)

        plt.figure(figsize=(24, 12))
        plt.subplot(1, 2, 1)
        plt.plot(epochs, train_loss, label="train loss")
        plt.plot(epochs, val_loss, label="valid loss")
        plt.xlabel("epoch")
        plt.ylabel("loss")
        plt.legend(loc="best")
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(epochs, train_acc, label="train accuracy")
        plt.plot(epochs, val_acc, label="valid accuracy")
        plt.xlabel("epoch")
        plt.ylabel("accuracy")
        plt.legend(loc="best")
        plt.grid(True)

        plt.savefig(path)


def predict(model, loader):
    model.eval()
    predictions = []
    answers = []
    with torch.no_grad():
        for data in loader:
            pred = model(data.x, data.edge_index, data.batch)
            for p in pred:
                predictions.append(p[1].numpy())
            for a in data.y:
                answers.append(a.numpy())

    return np.array(answers), np.array(predictions)


def prepare_roc(answers, predictions):
    fpr, tpr, _ = metrics.roc_curve(answers, predictions, pos_label=1)
    auc = metrics.auc(fpr, tpr)
    return (fpr, tpr, auc)


def plot_roc(fpr, tpr, auc, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    assert type(fpr) == dict
    assert type(tpr) == dict
    assert type(auc) == dict

    plt.figure(figsize=(12, 12))
    plt.title("ROC curve")
    plt.plot(tpr["train"], 1.-fpr["train"], "r--",
             label=f"Train ROC (AUC: {auc['train']:.3})")
    plt.plot(tpr["valid"], 1.-fpr["valid"], "b--",
             label=f"Validation ROC (AUC: {auc['valid']:.3})")
    plt.plot(tpr["test"], 1.-fpr["test"], "g--",
             label=f"Test ROC (AUC: {auc['test']:.3})")
    plt.legend(loc="best")
    plt.xlabel("sig eff.")
    plt.ylabel("bkg rej.")
    plt.savefig(path)

