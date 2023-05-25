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
combineTool.py -M Impacts -d workspace.root -m 125 --doInitialFit --setParameterRanges r=-2,2 -t -1
combineTool.py -M Impacts -d workspace.root -m 125 --doFits --setParameterRanges r=-2,2 -t -1
combineTool.py -M Impacts -d workspace.root -m 125 --setParameterRanges r=-2,2 -o impacts.json
plotImpacts.py -i impacts.json -o impacts --summary
cd $HOMEDIR
