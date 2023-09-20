#!/bin/sh
python evalModels.py --channel Skim3Mu --signal MHc-70_MA-65 --background nonprompt --epochs 90
python evalModels.py --channel Skim3Mu --signal MHc-100_MA-95 --background nonprompt --epochs 90
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-85 --background nonprompt --epochs 90
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-120 --background nonprompt --epochs 90
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-120 --background ttZ --epochs 90
