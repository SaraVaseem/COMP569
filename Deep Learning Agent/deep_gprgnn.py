# Model Definition

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_sparse import spmm
from torch_geometric.utils import add_self_loops, degree

class CustomDeepGPRGNN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, K=10, dropout=0.6, temperature=1.5):
        super(CustomDeepGPRGNN, self).__init__()
        self.K = K
        self.dropout = dropout
        self.temperature = temperature

        self.fc1 = nn.Linear(in_channels, hidden_channels)
        self.bn1 = nn.BatchNorm1d(hidden_channels)

        self.fc2 = nn.Linear(hidden_channels, hidden_channels)
        self.bn2 = nn.BatchNorm1d(hidden_channels)

        self.fc3 = nn.Linear(hidden_channels, hidden_channels)
        self.bn3 = nn.BatchNorm1d(hidden_channels)

        self.fc4 = nn.Linear(hidden_channels, out_channels)

        self.alpha = nn.Parameter(torch.Tensor(K + 1))
        nn.init.constant_(self.alpha, 1.0 / (K + 1))

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))

        row, col = edge_index
        deg = degree(row, x.size(0), dtype=x.dtype)
        deg_inv_sqrt = deg.pow(-0.5)
        deg_inv_sqrt[deg_inv_sqrt == float('inf')] = 0
        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]


        x0 = F.gelu(self.bn1(self.fc1(x)))
        x1 = F.gelu(self.bn2(self.fc2(F.dropout(x0, p=self.dropout, training=self.training))) + x0)
        x2 = F.gelu(self.bn3(self.fc3(F.dropout(x1, p=self.dropout, training=self.training))) + x1)
        x = self.fc4(F.dropout(x2, p=self.dropout, training=self.training))


        x_prop = self.alpha[0] * x
        x_temp = x
        for k in range(1, self.K + 1):
            x_temp = spmm(edge_index, norm, x.size(0), x.size(0), x_temp)
            x_prop += self.alpha[k] * x_temp

        return x_prop / self.temperature
