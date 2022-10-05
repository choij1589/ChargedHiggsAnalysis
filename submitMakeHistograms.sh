#!/bin/bash
era=$1
python scripts/submitMakeDataHistograms.py --era $1 --sample DoubleMuon &
python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-70_MA-15 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-70_MA-40 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-70_MA-65 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-100_MA-15 --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-100_MA-60 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-100_MA-95 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-130_MA-15 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-130_MA-55 --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-130_MA-90 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-130_MA-125 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-160_MA-15 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-160_MA-85 --split &
#python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-160_MA-120 --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample TTToHcToWAToMuMu_MHc-160_MA-155 --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample WZTo3LNu_amcatnlo --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample WZTo3LNu_mllmin4p0_powheg --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample ZZTo4L_powheg --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample DYJets --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample ZGToLLG --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample ttWToLNu --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample ttZToLLNuNu --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample ttHToNonbb --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample tZq --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample tHq --split & 
python scripts/submitMakeMCHistograms.py --era $1 --sample WWW --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample WWZ --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample WZZ --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample ZZZ --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample WWG --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample TTG --split & 
python scripts/submitMakeMCHistograms.py --era $1 --sample TTTT --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample VBF_HToZZTo4L --split &
python scripts/submitMakeMCHistograms.py --era $1 --sample GluGluHToZZTo4L --split &
