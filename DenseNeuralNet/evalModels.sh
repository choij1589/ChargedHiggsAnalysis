#!/bin/bash
CHANNEL=$1
BACKGROUND=$2

#python evalModels.py --channel $CHANNEL --signal MHc-70_MA-15 --background $BACKGROUND
#python evalModels.py --channel $CHANNEL --signal MHc-70_MA-40 --background $BACKGROUND
python evalModels.py --channel $CHANNEL --signal MHc-70_MA-65 --background $BACKGROUND
#python evalModels.py --channel $CHANNEL --signal MHc-100_MA-15 --background $BACKGROUND
#python evalModels.py --channel $CHANNEL --signal MHc-100_MA-60 --background $BACKGROUND
python evalModels.py --channel $CHANNEL --signal MHc-100_MA-95 --background $BACKGROUND
#python evalModels.py --channel $CHANNEL --signal MHc-130_MA-15 --background $BACKGROUND
#python evalModels.py --channel $CHANNEL --signal MHc-130_MA-55 --background $BACKGROUND
python evalModels.py --channel $CHANNEL --signal MHc-130_MA-90 --background $BACKGROUND
#python evalModels.py --channel $CHANNEL --signal MHc-130_MA-125 --background $BACKGROUND
#python evalModels.py --channel $CHANNEL --signal MHc-160_MA-15 --background $BACKGROUND
python evalModels.py --channel $CHANNEL --signal MHc-160_MA-85 --background $BACKGROUND
python evalModels.py --channel $CHANNEL --signal MHc-160_MA-120 --background $BACKGROUND
#python evalModels.py --channel $CHANNEL --signal MHc-160_MA-155 --background $BACKGROUND
