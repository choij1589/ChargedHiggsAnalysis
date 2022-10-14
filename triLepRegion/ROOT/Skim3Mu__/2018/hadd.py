import os

SAMPLEs = ["DoubleMuon",
           "TTToHcToWAToMuMu_MHc-70_MA-15",
           "TTToHcToWAToMuMu_MHc-100_MA-60",
           "TTToHcToWAToMuMu_MHc-130_MA-90",
           "TTToHcToWAToMuMu_MHc-160_MA-155",
           "WZTo3LNu_amcatnlo",
           "WZTo3LNu_mllmin4p0_powheg",
           "DYJets",
           "ZGToLLG",
           "ttWToLNu",
           "ttZToLLNuNu",
           "ttHToNonbb",
           "tZq",
           "tHq",
           "WWW",
           "WWZ",
           "WZZ",
           "ZZZ",
           "WWG",
           "TTG",
           "TTTT",
           "VBF_HToZZTo4L",
           "GluGluHToZZTo4L",
           "ZZTo4L_powheg"]

for sample in SAMPLEs:
    os.system(f"hadd {sample}.root {sample}_*.root")
    os.system(f"rm {sample}_*.root")
