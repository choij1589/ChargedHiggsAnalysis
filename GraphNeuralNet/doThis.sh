#!/bin/sh
python evalModels.py --channel Skim1E2Mu --signal MHc-70_MA-65 --background nonprompt --epochs 80
python evalModels.py --channel Skim1E2Mu --signal MHc-130_MA-90 --background nonprompt --epochs 80
python evalModels.py --channel Skim1E2Mu --signal MHc-160_MA-85 --background nonprompt --epochs 80
