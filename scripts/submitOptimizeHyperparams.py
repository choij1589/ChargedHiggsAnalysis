import os
import sys
import uuid
import argparse

# Sync arguments with triLepRegion/selectModels.py
parser = argparse.ArgumentParser()
parser.add_argument("--train", "-t", required=True, type=str, help="DNN / GNN")
parser.add_argument("--signal", "-s", required=True, type=str, help="Signal mass point")
parser.add_argument("--background", "-b", required=True, type=str, help="background")
parser.add_argument("--channel", "-c", required=True, type=str, help="channel")
args = parser.parse_args()

# make random string
process = uuid.uuid4().hex.upper()[:6]
condorBase = f"optim_{args.signal}_vs_{args.background}_{process}"

def makeSubmitJds():
    f = open(f"condor/{condorBase}/submit.jds", "w")
    f.write(f"executable = condor/{condorBase}/run.sh\n")
    f.write(f"jobbatchname = train_{args.train}_{args.signal}_vs_{args.background}_{args.channel}\n")
    f.write('+singularityimage = "/data6/Users/choij/Singularity/torch200"\n')
    f.write("requirements = HasSingularity\n")
    f.write("request_disk = 40 GB\n")
    f.write("request_memory = 100 GB\n")
    f.write("request_cpus = 20\n")
    f.write("request_gpus = 1\n")
    f.write(f"log = condor/{condorBase}/job.log\n")
    f.write(f"output = condor/{condorBase}/job.out\n")
    f.write(f"error = condor/{condorBase}/job.err\n")
    f.write("queue 1")
    f.close()

def makeRunSh():
    f = open(f"condor/{condorBase}/run.sh", "w")
    f.write("#/bin/bash\n")
    f.write('export WORKDIR="/data6/Users/choij/ChargedHiggsAnalysis"\n')
    f.write('export PYTHONPATH="${PYTHONPATH}:${WORKDIR}"\n')
    f.write('export PYTHONPATH="${PYTHONPATH}:${WORKDIR}/libPython"\n')
    f.write("cd $WORKDIR\n")
    f.write("source /opt/conda/bin/activate\n")
    f.write("conda activate torch\n")
    f.write(f"python {args.train}/optimizeHyperParams.py --signal {args.signal} --background {args.background} --channel {args.channel}")
    f.close()

if __name__ == "__main__":
    os.makedirs(f"condor/{condorBase}")
    print(f"Running condor job in condor/{condorBase}...")
    makeSubmitJds()
    makeRunSh()
    os.chmod(f"condor/{condorBase}/run.sh", 0o755)
    os.system(f"condor_submit condor/{condorBase}/submit.jds")
