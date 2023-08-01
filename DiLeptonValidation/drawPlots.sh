#!/bin/sh
ERA=$1

python plot.py --era $ERA --channel DYDiMu --key muons/1/pt
python plot.py --era $ERA --channel DYDiMu --key muons/1/eta
python plot.py --era $ERA --channel DYDiMu --key muons/1/phi
python plot.py --era $ERA --channel DYDiMu --key muons/2/pt
python plot.py --era $ERA --channel DYDiMu --key muons/2/eta
python plot.py --era $ERA --channel DYDiMu --key muons/2/phi
python plot.py --era $ERA --channel DYDiMu --key jets/1/pt
python plot.py --era $ERA --channel DYDiMu --key jets/1/eta
python plot.py --era $ERA --channel DYDiMu --key jets/1/phi
python plot.py --era $ERA --channel DYDiMu --key jets/2/pt
python plot.py --era $ERA --channel DYDiMu --key jets/2/eta
python plot.py --era $ERA --channel DYDiMu --key jets/2/phi
python plot.py --era $ERA --channel DYDiMu --key jets/3/pt
python plot.py --era $ERA --channel DYDiMu --key jets/3/eta
python plot.py --era $ERA --channel DYDiMu --key jets/3/phi
python plot.py --era $ERA --channel DYDiMu --key jets/size
python plot.py --era $ERA --channel DYDiMu --key bjets/size
python plot.py --era $ERA --channel DYDiMu --key pair/pt
python plot.py --era $ERA --channel DYDiMu --key pair/eta
python plot.py --era $ERA --channel DYDiMu --key pair/phi
python plot.py --era $ERA --channel DYDiMu --key pair/mass
python plot.py --era $ERA --channel DYDiMu --key METv/pt
python plot.py --era $ERA --channel DYDiMu --key METv/phi

python plot.py --era $ERA --channel DYDiMu --noSF --key muons/1/pt
python plot.py --era $ERA --channel DYDiMu --noSF --key muons/1/eta
python plot.py --era $ERA --channel DYDiMu --noSF --key muons/1/phi
python plot.py --era $ERA --channel DYDiMu --noSF --key muons/2/pt
python plot.py --era $ERA --channel DYDiMu --noSF --key muons/2/eta
python plot.py --era $ERA --channel DYDiMu --noSF --key muons/2/phi
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/1/pt
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/1/eta
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/1/phi
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/2/pt
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/2/eta
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/2/phi
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/3/pt
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/3/eta
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/3/phi
python plot.py --era $ERA --channel DYDiMu --noSF --key jets/size
python plot.py --era $ERA --channel DYDiMu --noSF --key bjets/size
python plot.py --era $ERA --channel DYDiMu --noSF --key pair/pt
python plot.py --era $ERA --channel DYDiMu --noSF --key pair/eta
python plot.py --era $ERA --channel DYDiMu --noSF --key pair/phi
python plot.py --era $ERA --channel DYDiMu --noSF --key pair/mass
python plot.py --era $ERA --channel DYDiMu --noSF --key METv/pt
python plot.py --era $ERA --channel DYDiMu --noSF --key METv/phi


python plot.py --era $ERA --channel TTDiMu --key muons/1/pt
python plot.py --era $ERA --channel TTDiMu --key muons/1/eta
python plot.py --era $ERA --channel TTDiMu --key muons/1/phi
python plot.py --era $ERA --channel TTDiMu --key muons/2/pt
python plot.py --era $ERA --channel TTDiMu --key muons/2/eta
python plot.py --era $ERA --channel TTDiMu --key muons/2/phi
python plot.py --era $ERA --channel TTDiMu --key jets/1/pt
python plot.py --era $ERA --channel TTDiMu --key jets/1/eta
python plot.py --era $ERA --channel TTDiMu --key jets/1/phi
python plot.py --era $ERA --channel TTDiMu --key jets/2/pt
python plot.py --era $ERA --channel TTDiMu --key jets/2/eta
python plot.py --era $ERA --channel TTDiMu --key jets/2/phi
python plot.py --era $ERA --channel TTDiMu --key jets/3/pt
python plot.py --era $ERA --channel TTDiMu --key jets/3/eta
python plot.py --era $ERA --channel TTDiMu --key jets/3/phi
python plot.py --era $ERA --channel TTDiMu --key jets/size
python plot.py --era $ERA --channel TTDiMu --key bjets/1/pt
python plot.py --era $ERA --channel TTDiMu --key bjets/1/eta
python plot.py --era $ERA --channel TTDiMu --key bjets/1/phi
python plot.py --era $ERA --channel TTDiMu --key bjets/2/pt
python plot.py --era $ERA --channel TTDiMu --key bjets/2/eta
python plot.py --era $ERA --channel TTDiMu --key bjets/2/phi
python plot.py --era $ERA --channel TTDiMu --key bjets/3/pt
python plot.py --era $ERA --channel TTDiMu --key bjets/3/eta
python plot.py --era $ERA --channel TTDiMu --key bjets/3/phi
python plot.py --era $ERA --channel TTDiMu --key bjets/size
python plot.py --era $ERA --channel TTDiMu --key pair/pt
python plot.py --era $ERA --channel TTDiMu --key pair/eta
python plot.py --era $ERA --channel TTDiMu --key pair/phi
python plot.py --era $ERA --channel TTDiMu --key pair/mass
python plot.py --era $ERA --channel TTDiMu --key METv/pt
python plot.py --era $ERA --channel TTDiMu --key METv/phi

python plot.py --era $ERA --channel TTDiMu --noSF --key muons/1/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key muons/1/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key muons/1/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key muons/2/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key muons/2/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key muons/2/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/1/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/1/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/1/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/2/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/2/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/2/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/3/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/3/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/3/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key jets/size
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/1/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/1/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/1/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/2/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/2/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/2/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/3/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/3/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/3/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key bjets/size
python plot.py --era $ERA --channel TTDiMu --noSF --key pair/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key pair/eta
python plot.py --era $ERA --channel TTDiMu --noSF --key pair/phi
python plot.py --era $ERA --channel TTDiMu --noSF --key pair/mass
python plot.py --era $ERA --channel TTDiMu --noSF --key METv/pt
python plot.py --era $ERA --channel TTDiMu --noSF --key METv/phi