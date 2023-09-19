#!/bin/sh
ERA=$1
MEASURE=$2

echo plotting for era $ERA, measure $MEASURE

# plot fake rate
python plotFakeRate.py --era $ERA --measure $MEASURE
python plotFakeRate.py --era $ERA --measure $MEASURE --isQCD
# plot prompt normalization
if [[ $MEASURE == "muon" ]]; then
    python plotPromptNorm.py --era $ERA --hlt MeasFakeMu8 --id loose
    python plotPromptNorm.py --era $ERA --hlt MeasFakeMu8 --id tight
    python plotPromptNorm.py --era $ERA --hlt MeasFakeMu17 --id loose
    python plotPromptNorm.py --era $ERA --hlt MeasFakeMu17 --id tight
elif [[ $MEASURE == "electron" ]]; then
    python plotPromptNorm.py --era $ERA --hlt MeasFakeEl8 --id loose
    python plotPromptNorm.py --era $ERA --hlt MeasFakeEl12 --id loose
    python plotPromptNorm.py --era $ERA --hlt MeasFakeEl23 --id loose
    python plotPromptNorm.py --era $ERA --hlt MeasFakeEl8 --id tight
    python plotPromptNorm.py --era $ERA --hlt MeasFakeEl12 --id tight
    python plotPromptNorm.py --era $ERA --hlt MeasFakeEl23 --id tight
else
    echo "Wrong measure $MEASURE"
    exit 1
fi
# plot systematics
python plotSystematics.py --era $ERA --measure $MEASURE --eta 1
python plotSystematics.py --era $ERA --measure $MEASURE --eta 2
python plotSystematics.py --era $ERA --measure $MEASURE --eta 3

