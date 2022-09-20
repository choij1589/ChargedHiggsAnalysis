#!/bin/bash
era=$1
python3 scripts/submitMakeDataHistograms.py --era $1 --sample DoubleMuon &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-70_MA-15 --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-70_MA-40 --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-70_MA-65 --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample WZTo3LNu_amcatnlo --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample WZTo3LNu_mllmin4p0_powheg --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample ZZTo4L_powheg --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample DYJets --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample ZGToLLG --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample ttWToLNu --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample ttZToLLNuNu --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample ttHToNonbb --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample tZq --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample tHq --split & 
python3 scripts/submitMakeMCHistograms.py --era $1 --sample WWW --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample WWZ --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample WZZ --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample ZZZ --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample WWG --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample TTG --split & 
python3 scripts/submitMakeMCHistograms.py --era $1 --sample TTTT --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample VBF_HToZZTo4L --split &
python3 scripts/submitMakeMCHistograms.py --era $1 --sample GluGluHToZZTo4L --split &
