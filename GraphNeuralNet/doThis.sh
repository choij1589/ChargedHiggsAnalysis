#!/bin/sh
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-85 --background nonprompt --epochs 80
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-120 --background nonprompt --epochs 80
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-120 --background ttZ --epochs 80
