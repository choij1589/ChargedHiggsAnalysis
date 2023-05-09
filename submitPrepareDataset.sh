#!/bin/bash
ERA=$1
CHANNEL=$2
SIGNAL=$3

python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample $SIGNAL
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample nonprompt
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample DYJets
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample DYJets10to50_MG
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample ZGToLLG
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample WZTo3LNu_amcatnlo
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample ZZTo4L_powheg
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample ttWToLNu
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample ttZToLLNuNu
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample ttHToNonbb
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample WWW
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample WWZ
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample WZZ
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample ZZZ
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample TTG
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample tZq
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample VBF_HToZZTo4L
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample GluGluHToZZTo4L
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample TTTT
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample WWG
python scripts/submitPrepareDataset.py --era $ERA --channel $CHANNEL --signal $SIGNAL --sample tHq
