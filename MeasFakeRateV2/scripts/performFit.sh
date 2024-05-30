#!/bin/bash
ERA=$1
HLT=$2

python performFit.py --era $ERA --hlt $HLT --wp loose --syst Central
python performFit.py --era $ERA --hlt $HLT --wp loose --syst RequireHeavyTag
python performFit.py --era $ERA --hlt $HLT --wp tight --syst Central
python performFit.py --era $ERA --hlt $HLT --wp tight --syst RequireHeavyTag
