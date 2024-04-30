import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Sequential, Linear, ReLU, Dropout, BatchNorm1d, ELU, AlphaDropout
from torch_geometric.nn import global_mean_pool, global_max_pool, knn_graph
from torch_geometric.nn import GCNConv, GraphConv, GATConv, SuperGATConv, TransformerConv
from torch_geometric.nn import GraphNorm
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import dropout_edge

class SNN(nn.Module):
    def __init__(self, nFeatures, nClasses, nNodes, dropout_p):
        super(SNN, self).__init__()
        # Lecun init is default for pytorch
        self.dropout_p = dropout_p
        self.bn = nn.BatchNorm1d(nFeatures)
        self.dense1 = nn.Linear(nFeatures, nNodes, bias=True)
        self.dense2 = nn.Linear(nNodes, nNodes, bias=True)
        self.dense3 = nn.Linear(nNodes, nNodes, bias=True)
        self.dense4 = nn.Linear(nNodes, nNodes, bias=True)
        self.dense5 = nn.Linear(nNodes, nNodes, bias=True)
        self.dense6 = nn.Linear(nNodes, nClasses, bias=True)
    
    def forward(self, x):
        x = F.selu(self.dense1(x))
        x = F.alpha_dropout(x, p=self.dropout_p, training=self.training)
        x = F.selu(self.dense2(x))
        x = F.alpha_dropout(x, p=self.dropout_p, training=self.training)
        x = F.selu(self.dense3(x))
        x = F.alpha_dropout(x, p=self.dropout_p, training=self.training)
        x = F.selu(self.dense4(x))
        x = F.alpha_dropout(x, p=self.dropout_p, training=self.training)
        x = F.selu(self.dense5(x))
        x = F.alpha_dropout(x, p=self.dropout_p, training=self.training)
        out = F.softmax(self.dense6(x), dim=1)
        
        return out


class GCN(nn.Module):
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
    
class GAT(nn.Module):
    def __init__(self, num_features, num_graph_features, num_hidden, num_classes, dropout_p):
        super(GAT, self).__init__()
        self.gn0 = GraphNorm(num_features)
        self.bn0 = BatchNorm1d(num_hidden+num_graph_features)
        self.conv1 = GATConv(in_channels=num_features, out_channels=num_hidden, heads=4, dropout=0.6)
        self.conv2 = GATConv(in_channels=num_hidden*4, out_channels=num_hidden, heads=4, dropout=0.6)
        self.conv3 = GATConv(in_channels=num_hidden*4, out_channels=num_hidden, dropout=0.6)
        self.dense1 = Linear(num_hidden+num_graph_features, num_hidden)
        self.dense2 = Linear(num_hidden, num_hidden)
        self.output = Linear(num_hidden, num_classes)
        self.dropout_p = dropout_p

    def forward(self, x, edge_index, graph_input,  batch=None):
        x = self.gn0(x, batch)
        x = F.dropout(x, p=0.6, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.6, training=self.training)
        x = F.elu(self.conv2(x, edge_index))
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv3(x, edge_index)
        
        # readout layers
        x = global_mean_pool(x, batch=batch)
        x = torch.cat([x, graph_input], dim=1)
        x = self.bn0(x)

        # dense layers
        x = F.alpha_dropout(x, p=self.dropout_p)
        x = F.selu(self.dense1(x))
        x = F.alpha_dropout(x, p=self.dropout_p)
        x = F.selu(self.dense2(x))
        x = self.output(x)

        return F.softmax(x, dim=1)


class GNN(nn.Module):
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
    
# NOTE: Using SELU activation layer in mlp block make training unstable
class EdgeConv(MessagePassing):
    def __init__(self, in_channels, out_channels, dropout_p):
        super().__init__(aggr="max")
        self.mlp = Sequential(
                Linear(2*in_channels, out_channels), ReLU(), BatchNorm1d(out_channels), Dropout(dropout_p),
                Linear(out_channels, out_channels), ReLU(), BatchNorm1d(out_channels), Dropout(dropout_p),
                Linear(out_channels, out_channels), ReLU(), BatchNorm1d(out_channels), Dropout(dropout_p)
                )

    def forward(self, x, edge_index, batch=None):
        return self.propagate(edge_index, x=x, batch=batch)

    def message(self, x_i, x_j):
        tmp = torch.cat([x_i, x_j - x_i], dim=1)
        return self.mlp(tmp)


class DynamicEdgeConv(EdgeConv):
    def __init__(self, in_channels, out_channels, dropout_p, training, k=4):
        super().__init__(in_channels, out_channels, dropout_p=dropout_p)
        self.shortcut = Sequential(Linear(in_channels, out_channels), BatchNorm1d(out_channels), Dropout(dropout_p))
        self.training = training
        self.k = k

    def forward(self, x, edge_index=None, batch=None):
        if edge_index is None:
            edge_index = knn_graph(x, self.k, batch, loop=False, flow=self.flow)
        edge_index, _ = dropout_edge(edge_index, p=0.2, training=self.training)
        out = super().forward(x, edge_index, batch=batch)
        out += self.shortcut(x)
        return out


class ParticleNetV3(torch.nn.Module):
    def __init__(self, num_node_features, num_graph_features, num_classes, num_hidden, dropout_p):
        super(ParticleNetV3, self).__init__()
        self.gn0 = GraphNorm(num_node_features)
        self.bn0 = BatchNorm1d(num_hidden+num_graph_features)
        self.conv1 = TransformerConv(num_node_features, num_hidden, beta=True, dropout_p=0.6, training=self.training)
        self.conv2 = DynamicEdgeConv(num_hidden, num_hidden, dropout_p=0.6, training=self.training, k=4)
        self.conv3 = DynamicEdgeConv(num_hidden, num_hidden, dropout_p=0.6, training=self.training, k=4)
        self.lin1 = Linear(3*num_hidden, num_hidden)
        self.dense1 = Linear(num_hidden+num_graph_features, num_hidden)
        self.dense2 = Linear(num_hidden, num_hidden)
        self.output = Linear(num_hidden, num_classes)
        self.dropout_p = dropout_p

    def forward(self, x, edge_index, graph_input, batch=None):
        # Convolution layers
        x = self.gn0(x, batch=batch)
        conv1 = F.elu(self.conv1(x, edge_index))
        conv2 = self.conv2(conv1, batch=batch)
        conv3 = self.conv3(conv2, batch=batch)
        x = conv1 + conv2 + conv3
        #x = self.lin1(torch.cat([conv1, conv2, conv3], dim=1))

        # readout layers
        x = global_mean_pool(x, batch=batch)
        x = torch.cat([x, graph_input], dim=1)
        x = self.bn0(x)
        
        # dense layers
        x = F.alpha_dropout(x, p=self.dropout_p)
        x = F.selu(self.dense1(x))
        x = F.alpha_dropout(x, p=self.dropout_p)
        x = F.selu(self.dense2(x))
        x = self.output(x)

        return F.log_softmax(x, dim=1)


class ParticleNet(torch.nn.Module):
    def __init__(self, num_features, num_classes, num_nodes, dropout_p):
        super(ParticleNet, self).__init__()
        self.gn0 = GraphNorm(num_features)
        self.conv1 = DynamicEdgeConv(num_features, num_nodes, dropout_p, training=self.training, k=4)
        self.conv2 = DynamicEdgeConv(num_nodes, num_nodes, dropout_p, training=self.training, k=4)
        self.conv3 = DynamicEdgeConv(num_nodes, num_nodes, dropout_p, training=self.training, k=4) 
        self.dense1 = Linear(num_nodes, num_nodes)
        self.bn1 = BatchNorm1d(num_nodes)
        self.dense2 = Linear(num_nodes, num_nodes)
        self.bn2 = BatchNorm1d(num_nodes)
        self.output = Linear(num_nodes, num_classes)
        self.dropout_p = dropout_p

    def forward(self, x, edge_index, batch=None):
        # Convolution layers
        x = self.gn0(x, batch=batch)
        conv1 = self.conv1(x, edge_index, batch=batch)
        conv2 = self.conv2(conv1, batch=batch)
        conv3 = self.conv3(conv2, batch=batch)
        x = conv1 + conv2 + conv3

        # readout layers
        x = global_mean_pool(x, batch=batch)

        # dense layers
        x = F.relu(self.dense1(x))
        x = self.bn1(x)
        x = F.dropout1d(x, p=self.dropout_p, training=self.training)
        x = F.relu(self.dense2(x))
        x = self.bn2(x)
        x = F.dropout1d(x, p=self.dropout_p, training=self.training)
        x = self.output(x)

        return F.softmax(x, dim=1)

class ParticleNetV2(torch.nn.Module):
    def __init__(self, num_node_features, num_graph_features, num_classes, num_hidden, dropout_p):
        super(ParticleNetV2, self).__init__()
        self.gn0 = GraphNorm(num_node_features)
        self.gn1 = GraphNorm(num_hidden)
        self.gn2 = GraphNorm(num_hidden)
        self.gn3 = GraphNorm(num_hidden)
        self.bn0 = BatchNorm1d(num_hidden+num_graph_features)
        self.bn1 = BatchNorm1d(num_hidden)
        self.bn2 = BatchNorm1d(num_hidden)
        self.conv1 = DynamicEdgeConv(num_node_features, num_hidden, dropout_p, training=self.training, k=4)
        self.conv2 = DynamicEdgeConv(num_hidden, num_hidden, dropout_p, training=self.training, k=4)
        self.conv3 = DynamicEdgeConv(num_hidden, num_hidden, dropout_p, training=self.training, k=4)
        self.lin = Linear(3*num_hidden, num_hidden)
        self.dense1 = Linear(num_hidden+num_graph_features, num_hidden)
        self.dense2 = Linear(num_hidden, num_hidden)
        self.output = Linear(num_hidden, num_classes)
        self.dropout_p = dropout_p

    def forward(self, x, edge_index, graph_input, batch=None):
        # Convolution layers
        x = self.gn0(x, batch=batch)
        conv1 = self.conv1(x, edge_index, batch=batch)
        conv1 = self.gn1(conv1, batch=batch)
        conv2 = self.conv2(conv1, batch=batch)
        conv2 = self.gn2(conv2, batch=batch)
        conv3 = self.conv3(conv2, batch=batch)
        conv3 = self.gn3(conv3, batch=batch)
        x = conv1 + conv2 + conv3

        # readout layers
        x = global_mean_pool(x, batch=batch)
        x = torch.cat([x, graph_input], dim=1)
        x = self.bn0(x)

        # dense layers
        x = F.relu(self.dense1(x))
        x = self.bn1(x)
        x = F.dropout1d(x, p=self.dropout_p, training=self.training)
        x = F.relu(self.dense2(x))
        x = self.bn2(x)
        x = F.dropout1d(x, p=self.dropout_p, training=self.training)
        x = self.output(x)
def forward(self, x, edge_index, graph_input, batch=None):
        # Convolution layers
        x = self.gn0(x, batch=batch)
        conv1 = self.conv1(x, edge_index, batch=batch)
        conv1 = self.gn1(conv1, batch=batch)
        conv2 = self.conv2(conv1, batch=batch)
        conv2 = self.gn2(conv2, batch=batch)
        conv3 = self.conv3(conv2, batch=batch)
        conv3 = self.gn3(conv3, batch=batch)
        x = conv1 + conv2 + conv3

        # readout layers
        x = global_mean_pool(x, batch=batch)
        x = torch.cat([x, graph_input], dim=1)
        x = self.bn0(x)

        # dense layers
        x = F.relu(self.dense1(x))
        x = self.bn1(x)
        x = F.dropout1d(x, p=self.dropout_p, training=self.training)
        x = F.relu(self.dense2(x))
        x = self.bn2(x)
        x = F.dropout1d(x, p=self.dropout_p, training=self.training)
        x = self.output(x)

        return F.softmax(x, dim=1)
        return F.softmax(x, dim=1)
