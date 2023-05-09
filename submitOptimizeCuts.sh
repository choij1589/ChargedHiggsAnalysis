#!/bin/sh
ERA=$1
CHANNEL=$2
NETWORK=$3

xsecs=(2 5 10 15)

for xsec in ${xsecs[@]}
do
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-70_MA-15 --network $NETWORK
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-70_MA-40 --network $NETWORK
    python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-70_MA-65 --network $NETWORK --xsec $xsec
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-100_MA-15 --network $NETWORK
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-100_MA-60 --network $NETWORK
    python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-100_MA-95 --network $NETWORK --xsec $xsec
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-130_MA-15 --network $NETWORK
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-130_MA-55 --network $NETWORK
    python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-130_MA-90 --network $NETWORK --xsec $xsec
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-130_MA-125 --network $NETWORK
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-160_MA-15 --network $NETWORK
    python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-160_MA-85 --network $NETWORK --xsec $xsec
    python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-160_MA-120 --network $NETWORK --xsec $xsec
    #python scripts/submitOptimizeCuts.py --era $ERA --channel $CHANNEL --signal MHc-160_MA-155 --network $NETWORK
done
