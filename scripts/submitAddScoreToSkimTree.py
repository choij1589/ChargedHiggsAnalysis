import os, sys
import uuid
import argparse

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("--sample", "-s", required=True, type=str, help="sample name")
parser.add_argument("--era", "-e", required=True, type=str, help="era")
args = parser.parse_args()

isData = args.sample in ["MuonEG", "DoubleMuon"]

# make random string
process = uuid.uuid4().hex.upper()[:6]
condorBase = f"{args.era}/score_{args.sample}_{process}"

# count number of samples
if isData:
    inputDir = f"/gv0/DATA/SKFlat/Run2UltraLegacy_v3/{args.era}/DATA_SkimTree_SS2lOR3l/{args.sample}"
else:
    inputDir = f"/gv0/DATA/SKFlat/Run2UltraLegacy_v3/{args.era}/MC_SkimTree_SS2lOR3l/{args.sample}"
inputDir = f"{inputDir}/{os.listdir(inputDir)[0]}"

def makeSubmitJds():
    f = open(f"condor/{condorBase}/submit.jds", "w")
    f.write(f"executable = condor/{condorBase}/run.sh\n")
    f.write(f"arguments = $(ProcID)\n")
    f.write('+singularityimage = "/data6/Users/choij/Singularity/torch"\n')
    f.write("requirements = HasSingularity\n")
    f.write("request_memory = 4 GB\n")
    f.write(f"log = condor/{condorBase}/job.log\n")
    f.write(f"output = condor/{condorBase}/job.out\n")
    f.write(f"error = condor/{condorBase}/job.err\n")
    f.write(f"queue {len(os.listdir(inputDir))}")
    f.close()

def makeRunSh():
    f = open(f"condor/{condorBase}/run.sh", "w")
    f.write("#/bin/bash\n")
    f.write(f"export SAMPLE={inputDir}/SKFlatNtuple_{args.era}_MC_$1.root\n")
    f.write('export WORKDIR="/data6/Users/choij/ChargedHiggsAnalysis"\n')
    f.write("cd $WORKDIR\n")
    f.write("source /opt/conda/bin/activate\n")
    f.write("conda activate torch\n")
    f.write(f"python triLepRegion/addScoreToSkimTree.py --era {args.era} --sample $SAMPLE")
    f.close()

if __name__ == "__main__":
    os.makedirs(f"condor/{condorBase}")
    print(f"Running condor job in condor/{condorBase}...")
    makeSubmitJds()
    makeRunSh()
    os.chmod(f"condor/{condorBase}/run.sh", 0o755)
    os.system(f"condor_submit condor/{condorBase}/submit.jds")

