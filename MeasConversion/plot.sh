#!/bin/sh
python plot.py --era 2016preVFP --channel Skim1E2Mu --key ZCand/mass
python plot.py --era 2016postVFP --channel Skim1E2Mu --key ZCand/mass
python plot.py --era 2017 --channel Skim1E2Mu --key ZCand/mass
python plot.py --era 2018 --channel Skim1E2Mu --key ZCand/mass

python plot.py --era 2016preVFP --channel Skim3Mu --key ZCand/mass
python plot.py --era 2016postVFP --channel Skim3Mu --key ZCand/mass
python plot.py --era 2017 --channel Skim3Mu --key ZCand/mass
python plot.py --era 2018 --channel Skim3Mu --key ZCand/mass

python plot.py --era 2016preVFP --channel Skim1E2Mu --key convLep/pt
python plot.py --era 2016postVFP --channel Skim1E2Mu --key convLep/pt
python plot.py --era 2017 --channel Skim1E2Mu --key convLep/pt
python plot.py --era 2018 --channel Skim1E2Mu --key convLep/pt

python plot.py --era 2016preVFP --channel Skim3Mu --key convLep/pt
python plot.py --era 2016postVFP --channel Skim3Mu --key convLep/pt
python plot.py --era 2017 --channel Skim3Mu --key convLep/pt
python plot.py --era 2018 --channel Skim3Mu --key convLep/pt

python plot.py --era 2016preVFP --channel Skim1E2Mu --key convLep/eta
python plot.py --era 2016postVFP --channel Skim1E2Mu --key convLep/eta
python plot.py --era 2017 --channel Skim1E2Mu --key convLep/eta
python plot.py --era 2018 --channel Skim1E2Mu --key convLep/eta

python plot.py --era 2016preVFP --channel Skim3Mu --key convLep/eta
python plot.py --era 2016postVFP --channel Skim3Mu --key convLep/eta
python plot.py --era 2017 --channel Skim3Mu --key convLep/eta
python plot.py --era 2018 --channel Skim3Mu --key convLep/eta

python plot.py --era 2016preVFP --channel Skim1E2Mu --key convLep/phi
python plot.py --era 2016postVFP --channel Skim1E2Mu --key convLep/phi
python plot.py --era 2017 --channel Skim1E2Mu --key convLep/phi
python plot.py --era 2018 --channel Skim1E2Mu --key convLep/phi

python plot.py --era 2016preVFP --channel Skim3Mu --key convLep/phi
python plot.py --era 2016postVFP --channel Skim3Mu --key convLep/phi
python plot.py --era 2017 --channel Skim3Mu --key convLep/phi
python plot.py --era 2018 --channel Skim3Mu --key convLep/phi
