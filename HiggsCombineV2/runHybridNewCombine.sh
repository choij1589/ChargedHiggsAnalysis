#!/bin/sh
ERA=$1
CHANNEL=$2
MASSPOINT=$3

HOMEDIR=$PWD
BASEDIR=${HOMEDIR}/results/FullRun2__/Skim3Mu__/${MASSPOINT}
echo $BASEDIR

# prepare datacard
combineCards.py era2016a=results/2016preVFP/Skim3Mu__/${MASSPOINT}/datacard.txt \
                era2016b=results/2016postVFP/Skim3Mu__/${MASSPOINT}/datacard.txt \
                era2017=results/2017/Skim3Mu__/${MASSPOINT}/datacard.txt \
                era2018=results/2018/Skim3Mu__/${MASSPOINT}/datacard.txt >> datacard.txt

mkdir -p $BASEDIR

# run combine
text2workspace.py datacard.txt -o workspace.root
combine -M AsymptoticLimits workspace.root -t -1
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 12
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.500     # median expected
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.840     # 68% up
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.160     # 68% down
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.975     # 95% up
combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t -1 --fork 12 --expectedFromGrid 0.025     # 95% down

# clean directory for the next run
mv datacard.txt $BASEDIR
mv workspace.root $BASEDIR
mv higgsCombineTest.*.root $BASEDIR
