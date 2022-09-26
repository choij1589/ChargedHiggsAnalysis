#!/bin/sh
#ERAs=( 2016preVFP 2016postVFP 2017 2018)
ERAs=( 2017 )
REGION=$1


echo drawing plots for the region $REGION...

if [ $REGION = "ZGammaRegion" ]
then
	for ERA in "${ERAs[@]}"
	do
		mkdir -p plots/${ERA}/${REGION}
		python drawPlots.py --era $ERA --var muons/1/pt --region $REGION
		python drawPlots.py --era $ERA --var muons/1/eta --region $REGION
		python drawPlots.py --era $ERA --var muons/1/phi --region $REGION
		python drawPlots.py --era $ERA --var muons/2/pt --region $REGION
		python drawPlots.py --era $ERA --var muons/2/eta --region $REGION
		python drawPlots.py --era $ERA --var muons/2/phi --region $REGION
		python drawPlots.py --era $ERA --var muons/3/pt --region $REGION
		python drawPlots.py --era $ERA --var muons/3/eta --region $REGION
		python drawPlots.py --era $ERA --var muons/3/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/1/pt --region $REGION
		python drawPlots.py --era $ERA --var jets/1/eta --region $REGION
		python drawPlots.py --era $ERA --var jets/1/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/1/mass --region $REGION
		python drawPlots.py --era $ERA --var jets/2/pt --region $REGION
		python drawPlots.py --era $ERA --var jets/2/eta --region $REGION
		python drawPlots.py --era $ERA --var jets/2/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/2/mass --region $REGION
		python drawPlots.py --era $ERA --var jets/3/pt --region $REGION
		python drawPlots.py --era $ERA --var jets/3/eta --region $REGION
		python drawPlots.py --era $ERA --var jets/3/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/3/mass --region $REGION
		python drawPlots.py --era $ERA --var jets/4/pt --region $REGION
		python drawPlots.py --era $ERA --var jets/4/eta --region $REGION
		python drawPlots.py --era $ERA --var jets/4/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/4/mass --region $REGION
		python drawPlots.py --era $ERA --var jets/size --region $REGION
		#python drawPlots.py --era $ERA --var jets/HT --region $REGION
		python drawPlots.py --era $ERA --var ZCand/mass --region $REGION
		python drawPlots.py --era $ERA --var ZCand/pt --region $REGION
		python drawPlots.py --era $ERA --var ZCand/eta --region $REGION
		python drawPlots.py --era $ERA --var ZCand/phi --region $REGION
		python drawPlots.py --era $ERA --var MHc-70_MA-15vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-70_MA-40vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-70_MA-65vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-100_MA-15vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-100_MA-60vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-100_MA-95vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-130_MA-15vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-130_MA-55vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-130_MA-90vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-130_MA-125vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-160_MA-15vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-160_MA-85vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-160_MA-120vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-160_MA-155vsTTLL_powheg/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-70_MA-15vsVV/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-70_MA-40vsVV/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-70_MA-65vsVV/score --region $REGION
		python drawPlots.py --era $ERA --var MHc-100_MA-15vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-100_MA-60vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-100_MA-95vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-15vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-55vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-90vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-125vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-15vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-85vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-120vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-155vsVV/score --region $REGION
	done
elif [ $REGION = "ZFakeRegion" ]
then
	for ERA in "${ERAs[@]}"
	do
		mkdir -p plots/${ERA}/${REGION}
		python drawPlots.py --era $ERA --var muons/1/pt --region $REGION
		python drawPlots.py --era $ERA --var muons/1/eta --region $REGION
		python drawPlots.py --era $ERA --var muons/1/phi --region $REGION
		python drawPlots.py --era $ERA --var muons/2/pt --region $REGION
		python drawPlots.py --era $ERA --var muons/2/eta --region $REGION
		python drawPlots.py --era $ERA --var muons/2/phi --region $REGION
		python drawPlots.py --era $ERA --var muons/3/pt --region $REGION
		python drawPlots.py --era $ERA --var muons/3/eta --region $REGION
		python drawPlots.py --era $ERA --var muons/3/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/1/pt --region $REGION
		python drawPlots.py --era $ERA --var jets/1/eta --region $REGION
		python drawPlots.py --era $ERA --var jets/1/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/1/mass --region $REGION
		python drawPlots.py --era $ERA --var jets/2/pt --region $REGION
		python drawPlots.py --era $ERA --var jets/2/eta --region $REGION
		python drawPlots.py --era $ERA --var jets/2/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/2/mass --region $REGION
		python drawPlots.py --era $ERA --var jets/3/pt --region $REGION
		python drawPlots.py --era $ERA --var jets/3/eta --region $REGION
		python drawPlots.py --era $ERA --var jets/3/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/3/mass --region $REGION
		python drawPlots.py --era $ERA --var jets/4/pt --region $REGION
		python drawPlots.py --era $ERA --var jets/4/eta --region $REGION
		python drawPlots.py --era $ERA --var jets/4/phi --region $REGION
		python drawPlots.py --era $ERA --var jets/4/mass --region $REGION
		python drawPlots.py --era $ERA --var jets/size --region $REGION
		#python drawPlots.py --era $ERA --var jets/HT --region $REGION
		python drawPlots.py --era $ERA --var ZCand/mass --region $REGION
		python drawPlots.py --era $ERA --var ZCand/pt --region $REGION
		python drawPlots.py --era $ERA --var ZCand/eta --region $REGION
		python drawPlots.py --era $ERA --var ZCand/phi --region $REGION
		python drawPlots.py --era $ERA --var xZCand/mass --region $REGION
		python drawPlots.py --era $ERA --var xZCand/pt --region $REGION
		python drawPlots.py --era $ERA --var xZCand/eta --region $REGION
		python drawPlots.py --era $ERA --var xZCand/phi --region $REGION
		python drawPlots.py --era $ERA --var MHc-70_MA-15vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-70_MA-40vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-70_MA-65vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-100_MA-15vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-100_MA-60vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-100_MA-95vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-15vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-55vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-90vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-125vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-15vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-85vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-120vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-155vsTTLL_powheg/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-70_MA-15vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-70_MA-40vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-70_MA-65vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-100_MA-15vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-100_MA-60vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-100_MA-95vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-15vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-55vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-90vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-130_MA-125vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-15vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-85vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-120vsVV/score --region $REGION
        python drawPlots.py --era $ERA --var MHc-160_MA-155vsVV/score --region $REGION
	done
else	#signalregion
	echo SignalRegion is not defined yet
fi
