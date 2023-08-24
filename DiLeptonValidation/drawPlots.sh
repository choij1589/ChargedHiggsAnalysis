#!/bin/sh
ERA=$1

python plot.py --era $ERA --channel DiMu --key muons/1/pt
python plot.py --era $ERA --channel DiMu --key muons/1/eta
python plot.py --era $ERA --channel DiMu --key muons/1/phi
python plot.py --era $ERA --channel DiMu --key muons/2/pt
python plot.py --era $ERA --channel DiMu --key muons/2/eta
python plot.py --era $ERA --channel DiMu --key muons/2/phi
python plot.py --era $ERA --channel DiMu --key jets/1/pt
python plot.py --era $ERA --channel DiMu --key jets/1/eta
python plot.py --era $ERA --channel DiMu --key jets/1/phi
python plot.py --era $ERA --channel DiMu --key jets/2/pt
python plot.py --era $ERA --channel DiMu --key jets/2/eta
python plot.py --era $ERA --channel DiMu --key jets/2/phi
python plot.py --era $ERA --channel DiMu --key jets/3/pt
python plot.py --era $ERA --channel DiMu --key jets/3/eta
python plot.py --era $ERA --channel DiMu --key jets/3/phi
python plot.py --era $ERA --channel DiMu --key jets/size
python plot.py --era $ERA --channel DiMu --key bjets/1/pt
python plot.py --era $ERA --channel DiMu --key bjets/1/eta
python plot.py --era $ERA --channel DiMu --key bjets/1/phi
python plot.py --era $ERA --channel DiMu --key bjets/2/pt
python plot.py --era $ERA --channel DiMu --key bjets/2/eta
python plot.py --era $ERA --channel DiMu --key bjets/2/phi
python plot.py --era $ERA --channel DiMu --key bjets/3/pt
python plot.py --era $ERA --channel DiMu --key bjets/3/eta
python plot.py --era $ERA --channel DiMu --key bjets/3/phi
python plot.py --era $ERA --channel DiMu --key bjets/size
python plot.py --era $ERA --channel DiMu --key pair/pt
python plot.py --era $ERA --channel DiMu --key pair/eta
python plot.py --era $ERA --channel DiMu --key pair/phi
python plot.py --era $ERA --channel DiMu --key pair/mass
python plot.py --era $ERA --channel DiMu --key METv/pt
python plot.py --era $ERA --channel DiMu --key METv/phi

python plot.py --era $ERA --channel DiMu --noSF --key muons/1/pt
python plot.py --era $ERA --channel DiMu --noSF --key muons/1/eta
python plot.py --era $ERA --channel DiMu --noSF --key muons/1/phi
python plot.py --era $ERA --channel DiMu --noSF --key muons/2/pt
python plot.py --era $ERA --channel DiMu --noSF --key muons/2/eta
python plot.py --era $ERA --channel DiMu --noSF --key muons/2/phi
python plot.py --era $ERA --channel DiMu --noSF --key jets/1/pt
python plot.py --era $ERA --channel DiMu --noSF --key jets/1/eta
python plot.py --era $ERA --channel DiMu --noSF --key jets/1/phi
python plot.py --era $ERA --channel DiMu --noSF --key jets/2/pt
python plot.py --era $ERA --channel DiMu --noSF --key jets/2/eta
python plot.py --era $ERA --channel DiMu --noSF --key jets/2/phi
python plot.py --era $ERA --channel DiMu --noSF --key jets/3/pt
python plot.py --era $ERA --channel DiMu --noSF --key jets/3/eta
python plot.py --era $ERA --channel DiMu --noSF --key jets/3/phi
python plot.py --era $ERA --channel DiMu --noSF --key jets/size
python plot.py --era $ERA --channel DiMu --noSF --key bjets/1/pt
python plot.py --era $ERA --channel DiMu --noSF --key bjets/1/eta
python plot.py --era $ERA --channel DiMu --noSF --key bjets/1/phi
python plot.py --era $ERA --channel DiMu --noSF --key bjets/2/pt
python plot.py --era $ERA --channel DiMu --noSF --key bjets/2/eta
python plot.py --era $ERA --channel DiMu --noSF --key bjets/2/phi
python plot.py --era $ERA --channel DiMu --noSF --key bjets/3/pt
python plot.py --era $ERA --channel DiMu --noSF --key bjets/3/eta
python plot.py --era $ERA --channel DiMu --noSF --key bjets/3/phi
python plot.py --era $ERA --channel DiMu --noSF --key bjets/size
python plot.py --era $ERA --channel DiMu --noSF --key pair/pt
python plot.py --era $ERA --channel DiMu --noSF --key pair/eta
python plot.py --era $ERA --channel DiMu --noSF --key pair/phi
python plot.py --era $ERA --channel DiMu --noSF --key pair/mass
python plot.py --era $ERA --channel DiMu --noSF --key METv/pt
python plot.py --era $ERA --channel DiMu --noSF --key METv/phi
