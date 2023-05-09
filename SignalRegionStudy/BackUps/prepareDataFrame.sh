#!/bin/bash
ERA=$1
CHANNEL=$2
NETWORK=$3

MASSPOINTs=( "MHc-70_MA-15" "MHc-70_MA-40" "MHc-70_MA-65"
             "MHc-100_MA-15" "MHc-100_MA-60" "MHc-100_MA-95"
             "MHc-130_MA-15" "MHc-130_MA-55" "MHc-130_MA-90" "MHc-130_MA-125"
             "MHc-160_MA-15" "MHc-160_MA-85" "MHc-160_MA-120" "MHc-160_MA-155" )

for MASSPOINT in ${MASSPOINTs[@]}
do
    python prepareDataFrame.py --era $ERA --channel $CHANNEL --signal $MASSPOINT --network $NETWORK
done
