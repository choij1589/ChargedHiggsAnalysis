import os
import subprocess

ERAs = ["2016preVFP", "2016postVFP", "2017", "2018"]
Conversion = ["DYJets", "ZGToLLG"]
VV = ["WZTo3LNu_mllmin4p0_powheg"]
ttX = ["ttWToLNu", "ttZToLLNuNu", "ttHToNonbb", "tZq", "tHq"]
Rare = ["WWW", "WWZ", "WZZ", "ZZZ","WWG", "TTG", "TTTT", "VBF_HToZZTo4L", "GluGluHToZZTo4L"]
MCSamples = Conversion+VV+ttX+Rare

#for era in ERAs:
#    procs = []
#    command = f"python makeTriLepHistograms.py --era {era} --sample DoubleMuon --isData"
#    proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#    procs.append(proc)
#    for sample in MCSamples:
#        command = f"python makeTriLepHistograms.py --era {era} --sample {sample}"
#        proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#        procs.append(proc)
#    
#    for proc in procs:
#        proc.communicate()
#        assert proc.returncode == 0

#### ZZTo4L_powheg takes too much time
procs = []
for era in ERAs:
    command = f"python makeTriLepHistograms.py --era {era} --sample ZZTo4L_powheg"
    proc = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    procs.append(proc)

for proc in procs:
    proc.communicate()
    assert proc.returncode == 0
