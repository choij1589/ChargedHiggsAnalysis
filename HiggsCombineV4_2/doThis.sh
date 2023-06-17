#!/bin/bash
ERA=$1
CHANNEL=$2

./runHybridNew.sh $ERA $CHANNEL CutNCount
./runHybridNew.sh $ERA $CHANNEL Shape
#./runHybridNew.sh $ERA $CHANNEL GNNOptim
