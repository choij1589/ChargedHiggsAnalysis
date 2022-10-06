#!/bin/sh
ERA=$1
REGION=$2
MASSPOINTs=( "MHc-70_MA-15" "MHc-100_MA-60" "MHc-130_MA-90" "MHc-160_MA-155")

echo drawing plots for $REGION in $ERA...

mkdir -p plots/$ERA/$REGION
# Inputs
python drawPlots.py --era $ERA --var Inputs/muons/1/pt --region $REGION  
python drawPlots.py --era $ERA --var Inputs/muons/1/eta --region $REGION
python drawPlots.py --era $ERA --var Inputs/muons/1/phi --region $REGION
python drawPlots.py --era $ERA --var Inputs/muons/2/pt --region $REGION
python drawPlots.py --era $ERA --var Inputs/muons/2/eta --region $REGION 
python drawPlots.py --era $ERA --var Inputs/muons/2/phi --region $REGION
python drawPlots.py --era $ERA --var Inputs/muons/3/pt --region $REGION
python drawPlots.py --era $ERA --var Inputs/muons/3/eta --region $REGION
python drawPlots.py --era $ERA --var Inputs/muons/3/phi --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/1/pt --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/1/eta --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/1/phi --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/1/mass --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/2/pt --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/2/eta --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/2/phi --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/2/mass --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/3/pt --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/3/eta --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/3/phi --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/3/mass --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/4/pt --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/4/eta --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/4/phi --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/4/mass --region $REGION
python drawPlots.py --era $ERA --var Inputs/jets/size --region $REGION
#python drawPlots.py --era $ERA --var jets/HT --region $REGION
python drawPlots.py --era $ERA --var Inputs/ZCand/mass --region $REGION
python drawPlots.py --era $ERA --var Inputs/ZCand/pt --region $REGION
python drawPlots.py --era $ERA --var Inputs/ZCand/eta --region $REGION
python drawPlots.py --era $ERA --var Inputs/ZCand/phi --region $REGION
python drawPlots.py --era $ERA --var Inputs/xZCand/mass --region $REGION
python drawPlots.py --era $ERA --var Inputs/xZCand/pt --region $REGION
python drawPlots.py --era $ERA --var Inputs/xZCand/eta --region $REGION
python drawPlots.py --era $ERA --var Inputs/xZCand/phi --region $REGION
# Outputs
for MP in "${MASSPOINTs[@]}"
do
    python drawPlots.py --era $ERA --var Outputs/$MP/ACand/mass --region $REGION
    python drawPlots.py --era $ERA --var Outputs/$MP/ACand/pt --region $REGION
    python drawPlots.py --era $ERA --var Outputs/$MP/ACand/eta --region $REGION
    python drawPlots.py --era $ERA --var Outputs/$MP/ACand/phi --region $REGION
    python drawPlots.py --era $ERA --var Outputs/$MP/xACand/mass --region $REGION
    python drawPlots.py --era $ERA --var Outputs/$MP/xACand/pt --region $REGION
    python drawPlots.py --era $ERA --var Outputs/$MP/xACand/eta --region $REGION
    python drawPlots.py --era $ERA --var Outputs/$MP/xACand/phi --region $REGION
    python drawPlots.py --era $ERA --var Outputs/$MP/score_vsTTLL_powheg --region $REGION
done
