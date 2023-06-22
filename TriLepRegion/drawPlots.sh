#!/bin/sh
ERA=$1
REGION=$2

if [[ $REGION == *"3Mu"* ]]; then
KEYs=(
    "muons/1/pt" "muons/1/eta" "muons/1/phi"
    "muons/2/pt" "muons/2/eta" "muons/2/phi"
    "muons/3/pt" "muons/3/eta" "muons/3/phi"
    "jets/1/pt" "jets/1/eta" "jets/1/phi" "jets/1/mass"
    "jets/2/pt" "jets/2/eta" "jets/2/phi" "jets/2/mass"
    "jets/3/pt" "jets/3/eta" "jets/3/phi" "jets/3/mass"
    "jets/4/pt" "jets/4/eta" "jets/4/phi" "jets/4/mass"
    "jets/5/pt" "jets/5/eta" "jets/5/phi" "jets/5/mass"
    "bjets/1/pt" "bjets/1/eta" "bjets/1/phi" "bjets/1/mass"
    "bjets/2/pt" "bjets/2/eta" "bjets/2/phi" "bjets/2/mass" 
    "bjets/3/pt" "bjets/3/eta" "bjets/3/phi" "bjets/3/mass"
    "jets/size" "bjets/size" "METv/pt" "METv/phi"
    "stack/pt" "stack/eta" "stack/phi" "stack/mass"
    "MHc-70_MA-65/score_nonprompt" "MHc-70_MA-65/score_diboson" "MHc-70_MA-65/score_ttZ"
    "MHc-100_MA-95/score_nonprompt" "MHc-100_MA-95/score_diboson" "MHc-100_MA-95/score_ttZ"
    "MHc-130_MA-90/score_nonprompt" "MHc-130_MA-90/score_diboson" "MHc-130_MA-90/score_ttZ"
    "MHc-160_MA-85/score_nonprompt" "MHc-160_MA-85/score_diboson" "MHc-160_MA-85/score_ttZ"
    "MHc-160_MA-120/score_nonprompt" "MHc-160_MA-120/score_diboson" "MHc-160_MA-120/score_ttZ"
)
elif [[ $REGION == *"1E2Mu"* ]]; then
KEYs=(
    "muons/1/pt" "muons/1/eta" "muons/1/phi"
    "muons/2/pt" "muons/2/eta" "muons/2/phi"
    "electrons/1/pt" "electrons/1/eta" "electrons/1/phi"
)
else
    echo Wrong region $REGION
fi

for KEY in ${KEYs[@]}
do
    if [[ $REGION == *"SR"* ]]; then
        python drawPlots.py --era $ERA --channel $REGION --key $KEY --blind
    else
        python drawPlots.py --era $ERA --channel $REGION --key $KEY
    fi
done
