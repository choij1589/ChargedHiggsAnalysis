#!/bin/sh
ERA=$1

python drawPlots.py --era $ERA --channel DYDiMu --key muons/1/pt
python drawPlots.py --era $ERA --channel DYDiMu --key muons/1/eta
python drawPlots.py --era $ERA --channel DYDiMu --key muons/1/phi
python drawPlots.py --era $ERA --channel DYDiMu --key muons/2/pt
python drawPlots.py --era $ERA --channel DYDiMu --key muons/2/eta
python drawPlots.py --era $ERA --channel DYDiMu --key muons/2/phi
python drawPlots.py --era $ERA --channel DYDiMu --key jets/1/pt
python drawPlots.py --era $ERA --channel DYDiMu --key jets/1/eta
python drawPlots.py --era $ERA --channel DYDiMu --key jets/1/phi
python drawPlots.py --era $ERA --channel DYDiMu --key jets/2/pt
python drawPlots.py --era $ERA --channel DYDiMu --key jets/2/eta
python drawPlots.py --era $ERA --channel DYDiMu --key jets/2/phi
python drawPlots.py --era $ERA --channel DYDiMu --key jets/3/pt
python drawPlots.py --era $ERA --channel DYDiMu --key jets/3/eta
python drawPlots.py --era $ERA --channel DYDiMu --key jets/3/phi
python drawPlots.py --era $ERA --channel DYDiMu --key jets/size
python drawPlots.py --era $ERA --channel DYDiMu --key bjets/size
python drawPlots.py --era $ERA --channel DYDiMu --key pair/pt
python drawPlots.py --era $ERA --channel DYDiMu --key pair/eta
python drawPlots.py --era $ERA --channel DYDiMu --key pair/phi
python drawPlots.py --era $ERA --channel DYDiMu --key pair/mass
python drawPlots.py --era $ERA --channel DYDiMu --key METv/pt
python drawPlots.py --era $ERA --channel DYDiMu --key METv/phi



python drawPlots.py --era $ERA --channel TTDiMu --key muons/1/pt
python drawPlots.py --era $ERA --channel TTDiMu --key muons/1/eta
python drawPlots.py --era $ERA --channel TTDiMu --key muons/1/phi
python drawPlots.py --era $ERA --channel TTDiMu --key muons/2/pt
python drawPlots.py --era $ERA --channel TTDiMu --key muons/2/eta
python drawPlots.py --era $ERA --channel TTDiMu --key muons/2/phi
python drawPlots.py --era $ERA --channel TTDiMu --key jets/1/pt
python drawPlots.py --era $ERA --channel TTDiMu --key jets/1/eta
python drawPlots.py --era $ERA --channel TTDiMu --key jets/1/phi
python drawPlots.py --era $ERA --channel TTDiMu --key jets/2/pt
python drawPlots.py --era $ERA --channel TTDiMu --key jets/2/eta
python drawPlots.py --era $ERA --channel TTDiMu --key jets/2/phi
python drawPlots.py --era $ERA --channel TTDiMu --key jets/3/pt
python drawPlots.py --era $ERA --channel TTDiMu --key jets/3/eta
python drawPlots.py --era $ERA --channel TTDiMu --key jets/3/phi
python drawPlots.py --era $ERA --channel TTDiMu --key jets/size
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/1/pt
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/1/eta
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/1/phi
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/2/pt
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/2/eta
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/2/phi
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/3/pt
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/3/eta
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/3/phi
python drawPlots.py --era $ERA --channel TTDiMu --key bjets/size
python drawPlots.py --era $ERA --channel TTDiMu --key pair/pt
python drawPlots.py --era $ERA --channel TTDiMu --key pair/eta
python drawPlots.py --era $ERA --channel TTDiMu --key pair/phi
python drawPlots.py --era $ERA --channel TTDiMu --key pair/mass
python drawPlots.py --era $ERA --channel TTDiMu --key METv/pt
python drawPlots.py --era $ERA --channel TTDiMu --key METv/phi
