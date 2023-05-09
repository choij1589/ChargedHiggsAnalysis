#!/bin/bash
TRAIN=$1
CHANNEL=$2
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-70_MA-65 --background nonprompt --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-100_MA-95 --background nonprompt --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-130_MA-90 --background nonprompt --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-160_MA-85 --background nonprompt --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-160_MA-120 --background nonprompt --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-70_MA-65 --background diboson --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-100_MA-95 --background diboson --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-130_MA-90 --background diboson --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-160_MA-85 --background diboson --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-160_MA-120 --background diboson --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-70_MA-65 --background ttZ --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-100_MA-95 --background ttZ --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-130_MA-90 --background ttZ --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-160_MA-85 --background ttZ --channel $CHANNEL
python scripts/submitOptimizeHyperparams.py --train $TRAIN --signal MHc-160_MA-120 --background ttZ --channel $CHANNEL
