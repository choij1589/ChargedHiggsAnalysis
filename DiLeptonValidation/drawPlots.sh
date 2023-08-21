#!/bin/sh
ERA=$1
CHANNEL=$2

python plot.py --era $ERA --channel $CHANNEL --key muons/1/pt
python plot.py --era $ERA --channel $CHANNEL --key muons/1/eta
python plot.py --era $ERA --channel $CHANNEL --key muons/1/phi
python plot.py --era $ERA --channel $CHANNEL --key muons/2/pt
python plot.py --era $ERA --channel $CHANNEL --key muons/2/eta
python plot.py --era $ERA --channel $CHANNEL --key muons/2/phi
python plot.py --era $ERA --channel $CHANNEL --key electrons/1/pt
python plot.py --era $ERA --channel $CHANNEL --key electrons/1/eta
python plot.py --era $ERA --channel $CHANNEL --key electrons/1/phi
python plot.py --era $ERA --channel $CHANNEL --key jets/1/pt
python plot.py --era $ERA --channel $CHANNEL --key jets/1/eta
python plot.py --era $ERA --channel $CHANNEL --key jets/1/phi
python plot.py --era $ERA --channel $CHANNEL --key jets/2/pt
python plot.py --era $ERA --channel $CHANNEL --key jets/2/eta
python plot.py --era $ERA --channel $CHANNEL --key jets/2/phi
python plot.py --era $ERA --channel $CHANNEL --key jets/3/pt
python plot.py --era $ERA --channel $CHANNEL --key jets/3/eta
python plot.py --era $ERA --channel $CHANNEL --key jets/3/phi
python plot.py --era $ERA --channel $CHANNEL --key jets/size
python plot.py --era $ERA --channel $CHANNEL --key bjets/1/pt
python plot.py --era $ERA --channel $CHANNEL --key bjets/1/eta
python plot.py --era $ERA --channel $CHANNEL --key bjets/1/phi
python plot.py --era $ERA --channel $CHANNEL --key bjets/2/pt
python plot.py --era $ERA --channel $CHANNEL --key bjets/2/eta
python plot.py --era $ERA --channel $CHANNEL --key bjets/2/phi
python plot.py --era $ERA --channel $CHANNEL --key bjets/3/pt
python plot.py --era $ERA --channel $CHANNEL --key bjets/3/eta
python plot.py --era $ERA --channel $CHANNEL --key bjets/3/phi
python plot.py --era $ERA --channel $CHANNEL --key bjets/size
python plot.py --era $ERA --channel $CHANNEL --key pair/pt
python plot.py --era $ERA --channel $CHANNEL --key pair/eta
python plot.py --era $ERA --channel $CHANNEL --key pair/phi
python plot.py --era $ERA --channel $CHANNEL --key pair/mass
python plot.py --era $ERA --channel $CHANNEL --key METv/pt
python plot.py --era $ERA --channel $CHANNEL --key METv/phi

python plot.py --era $ERA --channel $CHANNEL --noSF --key muons/1/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key muons/1/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key muons/1/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key muons/2/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key muons/2/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key muons/2/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key electrons/1/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key electrons/1/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key electrons/1/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/1/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/1/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/1/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/2/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/2/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/2/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/3/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/3/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/3/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key jets/size
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/1/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/1/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/1/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/2/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/2/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/2/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/3/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/3/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/3/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key bjets/size
python plot.py --era $ERA --channel $CHANNEL --noSF --key pair/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key pair/eta
python plot.py --era $ERA --channel $CHANNEL --noSF --key pair/phi
python plot.py --era $ERA --channel $CHANNEL --noSF --key pair/mass
python plot.py --era $ERA --channel $CHANNEL --noSF --key METv/pt
python plot.py --era $ERA --channel $CHANNEL --noSF --key METv/phi
