#!/bin/bash
CHANNEL=$1
python scripts/submitOptimizeHyperparameters.py --signal MHc-70_MA-15 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-70_MA-40 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-70_MA-65 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-100_MA-15 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-100_MA-60 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-100_MA-95 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-130_MA-15 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-130_MA-55 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-130_MA-90 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-130_MA-125 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-160_MA-15 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-160_MA-85 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-160_MA-120 --background TTLL_powheg --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-160_MA-155 --background TTLL_powheg --channel $CHANNEL

python scripts/submitOptimizeHyperparameters.py --signal MHc-70_MA-15 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-70_MA-40 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-70_MA-65 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-100_MA-15 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-100_MA-60 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-100_MA-95 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-130_MA-15 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-130_MA-55 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-130_MA-90 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-130_MA-125 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-160_MA-15 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-160_MA-85 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-160_MA-120 --background ttX --channel $CHANNEL
python scripts/submitOptimizeHyperparameters.py --signal MHc-160_MA-155 --background ttX --channel $CHANNEL
