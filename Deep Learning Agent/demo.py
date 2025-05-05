# Simulate loading the model into a desktop app

from deep_gprgnn import CustomDeepGPRGNN

# To Use PyG prebuilt Binaries:

# Install Python 3.11.7 and PyTorch 2.3.1

# Install Process:

# Option 1: Download python3.11 through deadsnakes ppa

# Option 2: (Ubuntu 25.04 doesn't have 3.11 in deadsnakes)
# Use pyenv to install 3.11 - https://github.com/pyenv/pyenv?tab=readme-ov-file#linuxunix
# pyenv install 3.11.7
# pyenv virtualenv 3.11.7 comp569-311
# pyenv local comp569-311

# Install the last PyTorch that had cu121 wheels
# pip install torch==2.3.1+cu121 \
#   -f https://download.pytorch.org/whl/cu121/torch_stable.html

# Then install matching PyG wheels
# pip install --no-build-isolation --prefer-binary \
#   torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric \
#   -f https://data.pyg.org/whl/torch-2.3.1+cu121.html

# Option 3: (MacOS) cuda is not available
# Follow pyenv steps up to before downloading pytorch
# Install CPU only torch: pip install torch==2.3.1
# brew install cmake libomp
# pip install --upgrade pip setuptools wheel \
#   && pip install --no-build-isolation torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric

# PyG does not have pre-created wheel binaries for MacOS. Have to build from source. Pytorch doesn't use anaconda anymore
# Running the model on CPU is much slower
# Note: MacOS CSPRNG random number generator produces less favorable boards/results than on Linux?


######################################################
# Loading the Dataset
######################################################

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_sparse import spmm
from torch_geometric.utils import add_self_loops, degree

# 1) Recreate the model object
model = CustomDeepGPRGNN(
    in_channels=7, # of features
    hidden_channels=128,
    out_channels=2, # of classes
    K=20,
    dropout=0.2,
    temperature=1.5
)

# 2) Load weights
model.load_state_dict(torch.load("deep_gprgnn.pth"))

# 3) Set to eval mode
model.eval()

# 4) Call `model(data)` in app

######################################################
# Generating a random minesweeper board
######################################################

import numpy as np # pip install numpy
import random

def generate_board_fixed(rows: int, cols: int, num_mines: int) -> np.ndarray:
    """
    Generate a Minesweeper board with exactly num_mines mines placed uniformly at random.

    Args:
        rows (int): Number of rows in the board.
        cols (int): Number of columns in the board.
        num_mines (int): Total number of mines to place (<= rows*cols).

    Returns:
        np.ndarray: A (rows x cols) array of 0/1 values (1 = mine, 0 = safe).
    """
    total_cells = rows * cols
    if num_mines > total_cells:
        raise ValueError("num_mines cannot exceed total number of cells")

    # 1) List all cell coordinates
    all_cells = [(r, c) for r in range(rows) for c in range(cols)]

    # 2) Randomly sample exactly num_mines distinct positions - random uniform
    mine_positions = random.sample(all_cells, num_mines)

    # 3) Build the binary board
    board = np.zeros((rows, cols), dtype=np.int64)
    for r, c in mine_positions:
        board[r, c] = 1

    return board

board_size = 8
num_mines = 10

# Fixed-mines board
board_fixed = generate_board_fixed(board_size, board_size, num_mines=10)
print(f"\nFixed-mines {board_size}x {board_size} board ({num_mines} mines):")
print(board_fixed)

######################################################
# Running the model on the board
######################################################

# Embedding a smaller board into the main 100x100 graph
# vs. only running on a small board (gnn wasn't trained on small graph)

import numpy as np
from torch_geometric.data import Data

# --- 1) Board of set size above(1 = mine, 0 = empty)
small = board_fixed

# --- 2) Embed into a 100×100 “large” board
H_big, W_big = 100, 100
large = np.zeros((H_big, W_big), dtype=np.int64)

# choose an offset (e.g. top‑left corner)
oi, oj = 0, 0
large[oi:oi+board_size, oj:oj+board_size] = small

# --- 3) Compute features over the entire 100×100
# Compute the 7‑dim one‑hot features - 
# For each cell, ook at its 8 neighbors in board, um up how many of those are mines, 
# and then one‑hot‑encode that count into a length‑7 vector
def minesweeper_features(board, F=7):
    H, W = board.shape
    feats = []
    for i in range(H):
        for j in range(W):
            i0, i1 = max(i-1, 0), min(i+2, H)
            j0, j1 = max(j-1, 0), min(j+2, W)
            k = int(board[i0:i1, j0:j1].sum() - board[i,j])
            vec = np.zeros(F, dtype=np.float32)
            vec[min(k, F-1)] = 1.0
            feats.append(vec)
    return np.vstack(feats)

x_full = minesweeper_features(large, 7)            # shape [10000,7]
x_full = torch.from_numpy(x_full)                  # FloatTensor

# --- 4) Build the 100×100 grid edge_index
edges = []
for i in range(H_big):
    for j in range(W_big):
        u = i*W_big + j
        for di in (-1,0,1):
            for dj in (-1,0,1):
                if di==0 and dj==0: continue
                ni, nj = i+di, j+dj
                if 0 <= ni < H_big and 0 <= nj < W_big:
                    v = ni*W_big + nj
                    edges.append([u, v])
edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

data_full = Data(
    x = x_full.float(),
    edge_index = edge_index
)

# Make predictions - take the k most likely cells for mines

import torch.nn.functional as F

# 1) Compute full‑graph logits & mine probs
model.eval()
with torch.no_grad():
    out_full = model(data_full)            # [10000, 2]
    probs    = F.softmax(out_full, dim=1)[:,1]  # [10000] P(mine)

# 2) Identify the flat indices of your 8×8 region
sub_indices = []
for i in range(oi, oi + board_size):
    for j in range(oj, oj + board_size):
        sub_indices.append(i * W_big + j)
sub_indices = torch.tensor(sub_indices, dtype=torch.long)  # length = 64

# 3) Pull out just those probabilities
sub_probs = probs[sub_indices]  # [64]

# Top - K (know the exact # of mines) vs. thresholding (% confidence)

# 4) Pick top‑k inside subgrid
k = 10
topk_vals, topk_idx_local = torch.topk(sub_probs, k)
# Convert back to global indices
topk_idx_global = sub_indices[topk_idx_local]  # [k]

# 5) Build a full‑graph mask, but only those global positions get True
mask = torch.zeros_like(probs, dtype=torch.bool)
mask[topk_idx_global] = True

# 6) Reshape and slice
grid_mask    = mask.view(H_big, W_big)  
subgrid_mask = grid_mask[oi:oi+board_size, oj:oj+board_size]

print(f"\nTop-{k} mines inside {board_size}×{board_size} board:")
print(subgrid_mask.int())

######################################################
# Performance Metrics on Prediction
######################################################

# pip install scikit-learn
from sklearn.metrics import confusion_matrix, classification_report
# pip install seaborn
import seaborn as sns
# pip install matplotlib
import matplotlib.pyplot as plt

# Calculate the performance metrics of that prediction

actual = board_fixed
predicted = subgrid_mask.int().cpu().numpy()

# Flatten to 1D arrays
actual_flat = actual.flatten()
pred_flat = predicted.flatten()

# Compute metrics
print("Classification Report:")
print(classification_report(actual_flat, pred_flat, target_names=["Safe (0)", "Mine (1)"], digits=4))

print("Confusion Matrix:")
print(confusion_matrix(actual_flat, pred_flat))

cm = confusion_matrix(actual_flat, pred_flat)