#!/bin/sh
if [[ $HOSTNAME == *"tamsa2"* ]]; then
    echo "@@@@ Working on tamsa2"
    export WORKDIR="/data6/Users/choij/ChargedHiggsAnalysis"

    # Cuda setup
    #source /cvmfs/sft.cern.ch/lcg/releases/cuda/11.4-166ec/x86_64-centos7-gcc8-opt/setup.sh
    #source /cvmfs/sft.cern.ch/lcg/releases/cudnn/8.2.4.15-ca3b5/x86_64-centos7-gcc8-opt/cudnn-env.sh

    # Python setup
    source /cvmfs/sft.cern.ch/lcg/releases/LCG_102cuda/Python/3.9.12/x86_64-centos7-gcc8-opt/Python-env.sh
    #source /cvmfs/sft.cern.ch/lcg/releases/LCG_102cuda/pip/22.0.4/x86_64-centos7-gcc8-opt/pip-env.sh
    #source /cvmfs/sft.cern.ch/lcg/releases/LCG_102cuda/blas/0.3.20.openblas/x86_64-centos7-gcc8-opt/blas-env.sh
    # ROOT setup
    #source /cvmfs/sft.cern.ch/lcg/releases/LCG_102cuda/tbb/2020_U2/x86_64-centos7-gcc8-opt/tbb-env.sh
    #source /cvmfs/sft.cern.ch/lcg/releases/LCG_102cuda/ROOT/6.26.04/x86_64-centos7-gcc8-opt/ROOT-env.sh
    
    # install torch and torch_geometric
    #pip install --user torch==1.12.1+cu113 --extra-index-url https://download.pytorch.org/whl/cu113
    #pip install --user torch-scatter==2.0.9 torch-sparse==0.6.15 torch-cluster==1.6.0 torch-spline-conv==1.2.1 torch-geometric -f https://data.pyg.org/whl/torch-1.12.1+cu113.html

elif [[ $HOSTNAME == fedora ]]; then
    echo "@@@@ Working in local"
    export WORKDIR="/home/choij/workspace/ChargedHiggsAnalysis"
    source /home/choij/miniconda3/bin/activate
    conda activate hep
fi

alias splitFile="${WORKDIR}/libCpp/splitFile"
alias copyFile="${WORKDIR}/libCpp/copyFile"
