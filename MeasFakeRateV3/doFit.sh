#!/bin/sh
ERA=$1

python evalPromptNorm.py --era $ERA --hlt MeasFakeMu8 --id loose
python evalPromptNorm.py --era $ERA --hlt MeasFakeMu17 --id loose
python evalPromptNorm.py --era $ERA --hlt MeasFakeEl8 --id loose
python evalPromptNorm.py --era $ERA --hlt MeasFakeEl12 --id loose
python evalPromptNorm.py --era $ERA --hlt MeasFakeEl23 --id loose

python evalPromptNorm.py --era $ERA --hlt MeasFakeMu8 --id tight
python evalPromptNorm.py --era $ERA --hlt MeasFakeMu17 --id tight
python evalPromptNorm.py --era $ERA --hlt MeasFakeEl8 --id tight
python evalPromptNorm.py --era $ERA --hlt MeasFakeEl12 --id tight
python evalPromptNorm.py --era $ERA --hlt MeasFakeEl23 --id tight
