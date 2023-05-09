#!/bin/sh
ERA=$1
CHANNEL=$2
NETWORK=$3

#MASSPOINTs=( "MHc-70_MA-15" "MHc-70_MA-40" "MHc-70_MA-65"
#             "MHc-100_MA-15" "MHc-100_MA-60" "MHc-100_MA-95"
#             "MHc-130_MA-15" "MHc-130_MA-55" "MHc-130_MA-90" "MHc-130_MA-125"
#             "MHc-160_MA-15" "MHc-160_MA-85" "MHc-160_MA-120" "MHc-160_MA-155")

MASSPOINTs=( "MHc-70_MA-65" "MHc-160_MA-85" "MHc-130_MA-90" "MHc-100_MA-95" "MHc-160_MA-120")

for mp in ${MASSPOINTs[@]}
do
    #python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey $mp
    #python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey nonprompt
    #python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey conversion
    #python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey diboson
    #python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey ttX
    #python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey others

    python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey $mp --doCut
    python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey nonprompt --doCut
    python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey conversion --doCut
    python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey diboson --doCut
    python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey ttX --doCut
    python scripts/submitPrepareDatacard.py --era $ERA --channel $CHANNEL --signal $mp --network $NETWORK --sampleKey others --doCut
done
