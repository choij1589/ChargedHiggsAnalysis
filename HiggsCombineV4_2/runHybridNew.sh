#!/bin/sh

ERA=$1
CHANNEL=$2
METHOD=$3

if [ $METHOD == "GNNOptim" ]
then
  MASSPOINTs=( "MHc-70_MA-65" "MHc-160_MA-85" "MHc-130_MA-90" "MHc-100_MA-95" "MHc-160_MA-120")
else
  MASSPOINTs=( "MHc-70_MA-15" "MHc-70_MA-40" "MHc-70_MA-65"
			   "MHc-100_MA-15" "MHc-100_MA-60" "MHc-100_MA-95"
               "MHc-130_MA-15" "MHc-130_MA-55" "MHc-130_MA-90" "MHc-130_MA-125"
               "MHc-160_MA-15" "MHc-160_MA-85" "MHc-160_MA-120" "MHc-160_MA-155")
fi

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
	text2workspace.py datacard.txt -o workspace.root
    combine -M AsymptoticLimits workspace.root -t -1
    combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 18 --expectedFromGrid 0.025     # 95% down
    combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 18 --expectedFromGrid 0.160     # 68% down
    combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 18 --expectedFromGrid 0.500     # median
    combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 18 --expectedFromGrid 0.840     # 68% up
    combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 18 --expectedFromGrid 0.975     # 95% up
    combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 18

    cd $HOMEDIR
done
