#!/bin/bash
export WORKDIR="/data6/Users/choij/ChargedHiggsAnalysis"
cd $WORKDIR
source /opt/conda/bin/activate
conda activate torch
python optimizeHyperParams.py
