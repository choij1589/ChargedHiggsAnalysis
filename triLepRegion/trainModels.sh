#!/bin/sh
python trainModels.py --signal MHc-70_MA-15 --background TTLL_powheg --batch_size 512 --optimizer Adam --initial_lr 0.005 --scheduler ExponentialLR --hidden_layers 128
python trainModels.py --signal MHc-100_MA-60 --background TTLL_powheg --batch_size 512 --optimizer Adam --initial_lr 0.005 --scheduler ExponentialLR --hidden_layers 128
python trainModels.py --signal MHc-130_MA-90 --background TTLL_powheg --batch_size 512 --optimizer Adam --initial_lr 0.01 --scheduler ExponentialLR --hidden_layers 128
python trainModels.py --signal MHc-160_MA-155 --background TTLL_powheg --batch_size 512 --optimizer Adam --initial_lr 0.01 --scheduler ExponentialLR --hidden_layers 128
