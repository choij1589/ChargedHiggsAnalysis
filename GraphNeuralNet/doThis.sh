#!/bin/sh
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-120 --background nonprompt
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-85 --background ttZ
python evalModels.py --channel Skim3Mu --signal MHc-160_MA-120 --background ttZ
