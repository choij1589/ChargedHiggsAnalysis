#!/bin/sh
MASSPOINTs=(
	MHc-70_MA-15 MHc-70_MA-40 MHc-70_MA-65
	MHc-100_MA-15 MHc-100_MA-60 MHc-100_MA-95 
	MHc-130_MA-15 MHc-130_MA-55 MHc-130_MA-90 MHc-130_MA-125
	MHc-160_MA-15 MHc-160_MA-85 MHc-160_MA-120 MHc-160_MA-155
)

for mp in "${MASSPOINTs[@]}"
do
	file="Selector_TTToHcToWAToMuMu_${mp}.root"
	hadd $file 2016preVFP/Skim3Mu__/$file 2016postVFP/Skim3Mu__/$file 2017/Skim3Mu__/$file 2018/Skim3Mu__/$file
done
