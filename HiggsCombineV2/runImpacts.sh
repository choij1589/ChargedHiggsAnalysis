#!/bin/sh

ERA=$1
CHANNEL=$2
MASSPOINT=$3

HOMEDIR=$PWD
BASEDIR=${HOMEDIR}/results/${ERA}/${CHANNEL}__/${MASSPOINT}
echo $BASEDIR

# prepare datacard
cd $BASEDIR

# run combine
combineTool.py -M Impacts -d workspace.root -m 125 --doInitialFit -t -1
combineTool.py -M Impacts -d workspace.root -m 125 --doFits -t -1
combineTool.py -M Impacts -d workspace.root -m 125 -o impacts.json
plotImpacts.py -i impacts.json -o impacts
cd $HOMEDIR
