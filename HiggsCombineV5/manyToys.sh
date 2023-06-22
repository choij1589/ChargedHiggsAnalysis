#!/bin/bash

MASSPOINTs=( "MHc-70_MA-15" "MHc-70_MA-40" "MHc-130_MA-55" "MHc-100_MA-60" "MHc-70_MA-65" "MHc-160_MA-120" "MHc-130_MA-125" "MHc-160_MA-155")

for MASSPOINT in ${MASSPOINTs[@]}
do
  HOMEDIR=$PWD
  BASEDIR=${HOMEDIR}/results/2018/Skim3Mu__Shape__/${MASSPOINT}
  cd $BASEDIR
  combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t 10 --fork 18 --expectedFromGrid 0.025
  cd $HOMEDIR
done

MASSPOINTs=( "MHc-70_MA-65" "MHc-100_MA-95" "MHc-130_MA-125")
for MASSPOINT in ${MASSPOINTs[@]}
do
  HOMEDIR=$PWD
  BASEDIR=${HOMEDIR}/results/2018/Skim3Mu__GNNOptim__/${MASSPOINT}
  cd $BASEDIR
  combine -M HybridNew --LHCmode LHC-limits workspace.root --saveHybridResult -t 10 --fork 18 --expectedFromGrid 0.025
  cd $HOMEDIR
done
