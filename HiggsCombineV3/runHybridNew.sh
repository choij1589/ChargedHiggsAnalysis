#!/bin/sh

ERA=$1
CHANNEL=$2
NETWORK=$3
MASSPOINT=$4

HOMEDIR=$PWD
BASEDIR=${HOMEDIR}/results/${ERA}/${CHANNEL}__${NETWORK}__/${MASSPOINT}
echo $BASEDIR

# prepare datacard
mkdir -p $BASEDIR
echo python3 createCard.py --era $ERA --channel $CHANNEL --network $NETWORK --masspoint $MASSPOINT
python3 createCard.py --era $ERA --channel $CHANNEL --network $NETWORK --masspoint $MASSPOINT >> ${BASEDIR}/datacard.txt
cd $BASEDIR

# run combine
text2workspace.py datacard.txt -o workspace.root
combine -M AsymptoticLimits workspace.root -t -1
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 6
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 6 --expectedFromGrid 0.500     # median expected
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 6 --expectedFromGrid 0.840     # 68% up
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 6 --expectedFromGrid 0.160     # 68% down
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 6 --expectedFromGrid 0.975     # 95% up
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 6 --expectedFromGrid 0.025     # 95% down
#combineTool.py -M Impacts -d workspace.root -m 125 --doInitialFit -t -1
#combineTool.py -M Impacts -d workspace.root -m 125 --doFits -t -1
#combineTool.py -M Impacts -d workspace.root -m 125 -o impacts.json
#plotImpacts.py -i impacts.json -o impacts
cd $HOMEDIR
