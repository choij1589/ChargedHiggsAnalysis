#!/bin/sh

ERA=$1
CHANNEL=$2
MASSPOINT=$3

HOMEDIR=$PWD
BASEDIR=${HOMEDIR}/results/${ERA}/${CHANNEL}__/${MASSPOINT}
# prepare datacard
mkdir -p $BASEDIR
python3 createCard.py --era $ERA --channel $CHANNEL --masspoint $MASSPOINT >> ${BASEDIR}/datacard.txt
cd ${BASEDIR}

# run combine
combine -M AsymptoticLimits datacard.txt -t -1
combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12
combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.500     # median expected
combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.840     # 68% up
combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.160     # 68% down
combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.975     # 95% up
combine -M HybridNew --LHCmode LHC-limits datacard.txt --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.025     # 95% down
cd $HOMEDIR
