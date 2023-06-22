#!/bin/bash
ERA=$1
CHANNEL=$2

python reOptimSignal.py --era $ERA --channel $CHANNEL --signal MHc-70_MA-65 &
python reOptimSignal.py --era $ERA --channel $CHANNEL --signal MHc-100_MA-95 &
python reOptimSignal.py --era $ERA --channel $CHANNEL --signal MHc-130_MA-90 &
python reOptimSignal.py --era $ERA --channel $CHANNEL --signal MHc-160_MA-85 &
python reOptimSignal.py --era $ERA --channel $CHANNEL --signal MHc-160_MA-120 &
