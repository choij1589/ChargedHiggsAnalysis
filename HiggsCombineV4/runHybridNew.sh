#!/bin/sh

ERA=$1
CHANNEL=$2
METHOD=$3

MASSPOINTs=( "MHc-70_MA-15" "MHc-70_MA-40" "MHc-70_MA-65"
#            "MHc-100_MA-15" "MHc-100_MA-60" "MHc-100_MA-95"
             "MHc-130_MA-15" "MHc-130_MA-55" "MHc-130_MA-90" "MHc-130_MA-125"
             "MHc-160_MA-15" "MHc-160_MA-85" "MHc-160_MA-120" "MHc-160_MA-155")

#MASSPOINTs=( "MHc-70_MA-65" "MHc-160_MA-85" "MHc-130_MA-90" "MHc-100_MA-95" "MHc-160_MA-120")

for MASSPOINT in ${MASSPOINTs[@]}
do
    echo extracting limit for $MASSPOINT...
    HOMEDIR=$PWD
    BASEDIR=${HOMEDIR}/results/${ERA}/${CHANNEL}__${METHOD}__/${MASSPOINT}
    # prepare datacard
    mkdir -p $BASEDIR
    python3 createCard.py --era $ERA --channel $CHANNEL --masspoint $MASSPOINT --method $METHOD >> ${BASEDIR}/datacard.txt
    cd ${BASEDIR}

    # run combine
    combine -M AsymptoticLimits datacard.txt -t -1
    combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.025     # 95% down
    combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.160     # 68% down
    combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.500     # median expected
    combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.840     # 68% up
    combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.975     # 95% up
    combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12

    cd $HOMEDIR
done
