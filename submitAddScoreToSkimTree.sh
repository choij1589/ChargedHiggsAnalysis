#!/bin/bash
ERA=$1
# signal
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-70_MA-15_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-70_MA-40_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-70_MA-65_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-100_MA-15_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-100_MA-60_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-100_MA-95_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-130_MA-15_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-130_MA-55_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-130_MA-90_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-130_MA-125_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-160_MA-15_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-160_MA-85_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-160_MA-120_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTToHcToWAToMuMu_MHc-160_MA-155_MultiLepFilter_TuneCP5_13TeV-madgraph-pythia8 --era $ERA
# DY, ZG
python scripts/submitAddScoreToSkimTree.py --sample DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8 --era $ERA
# TT, TT+X
python scripts/submitAddScoreToSkimTree.py --sample TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8 --era $ERA
# python scripts/submitAddScoreToSkimTree.py --sample ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8 --era $ERA
# VV
python scripts/submitAddScoreToSkimTree.py --sample ZZTo4L_TuneCP5_13TeV_powheg_pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8 --era $ERA
# rare
python scripts/submitAddScoreToSkimTree.py --sample GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample WWG_TuneCP5_13TeV-amcatnlo-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample WZZ_TuneCP5_13TeV-amcatnlo-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample ZZZ_TuneCP5_13TeV-amcatnlo-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8 --era $ERA
python scripts/submitAddScoreToSkimTree.py --sample THQ_ctcvcp_4f_Hincl_TuneCP5_13TeV_madgraph_pythia8 --era $ERA
