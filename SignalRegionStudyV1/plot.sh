#!/bin/bash
ERA=$1
REGION=$2

if [[ $REGION == "SR1E2Mu" ]]; then
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/1/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/1/eta --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/1/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/2/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/2/eta --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/2/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key electrons/1/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key electrons/1/eta --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key electrons/1/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/eta --blind 
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/mass --blind
    #python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/charge --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/eta --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/mass --blind
    #python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/charge --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/eta --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/mass --blind
    #python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/charge --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/size --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key METv/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key METv/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/1/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/1/eta --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/1/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/2/mass --blind
    #python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/2/charge --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/2/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/2/eta --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/2/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/2/mass --blind
    #python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/2/charge --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key bjets/size --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key pair/mass --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key pair/pt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key pair/eta --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key pair/phi --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-100_MA-95/score_nonprompt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-100_MA-95/score_diboson --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-100_MA-95/score_ttZ --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-130_MA-90/score_nonprompt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-130_MA-90/score_diboson --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-130_MA-90/score_ttZ --blind --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-160_MA-85/score_nonprompt --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-160_MA-85/score_diboson --blind
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key MHc-160_MA-85/score_ttZ --blind
fi
    
if [[ $REGION == "ZFake1E2Mu" ]]; then
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/1/pt
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/1/eta
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/1/phi
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/2/pt
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/2/eta
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key muons/2/phi
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key electrons/1/pt
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key electrons/1/eta
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key electrons/1/phi
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/pt
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/eta
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/phi
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/mass
    #python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/1/charge
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/pt
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/eta
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/phi
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/mass
    #python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/2/charge
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/pt
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/eta
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/phi
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/mass
    #python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/3/charge
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key jets/size
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key METv/pt
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key METv/phi        
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key ZCand/mass
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key ZCand/pt
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key ZCand/eta
    python plot.py --era $ERA --channel Skim1E2Mu --region $REGION --key ZCand/phi 
fi

if [[ $REGION == "SR3Mu" ]]; then
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/1/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/1/eta --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/1/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/2/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/2/eta --blind 
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/2/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/3/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/3/eta --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/3/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/eta --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/mass --blind
    #python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/charge --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/eta --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/mass --blind
    #python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/charge --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/eta --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/mass --blind
    #python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/charge --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/size --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key METv/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key METv/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/1/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/1/eta --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/1/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/2/mass --blind
    #python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/2/charge --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/2/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/2/eta --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/2/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/2/mass --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/2/charge --blind
    #python plot.py --era $ERA --channel Skim3Mu --region $REGION --key bjets/size --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key stack/mass --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key stack/pt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key stack/eta --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key stack/phi --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-100_MA-95/score_nonprompt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-100_MA-95/score_diboson --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-100_MA-95/score_ttZ --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-130_MA-90/score_nonprompt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-130_MA-90/score_diboson --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-130_MA-90/score_ttZ --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-160_MA-85/score_nonprompt --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-160_MA-85/score_diboson --blind
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key MHc-160_MA-85/score_ttZ --blind
fi

if [[ $REGION == "ZFake3Mu" ]]; then
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/1/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/1/eta
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/1/phi
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/2/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/2/eta
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/2/phi
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/3/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/3/eta
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key muons/3/phi
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/eta
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/phi
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/mass
    #python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/1/charge
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/eta
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/phi
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/mass
    #python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/2/charge
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/eta
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/phi
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/mass
    #python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/3/charge
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key jets/size
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key METv/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key METv/phi
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key ZCand/mass
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key ZCand/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key ZCand/eta
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key ZCand/phi
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key nZCand/mass
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key nZCand/pt
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key nZCand/eta
    python plot.py --era $ERA --channel Skim3Mu --region $REGION --key nZCand/phi
fi
