import os
import sys
import uuid
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--signal", required=True, type=str, help="signal masspoint")
parser.add_argument("--network", required=True, type=str, help="network")
parser.add_argument("--xsec", required=True, type=str, help="signal xsec")
args = parser.parse_args()

# make random string
process = uuid.uuid4().hex.upper()[:6]
condorBase = f"optimizeCuts/{args.era}/{args.channel}__{args.network}__/{args.signal}_{process}"

def makeSubmitJds():
    jobbatchname = f"optimizeCuts_{args.era}_{args.channel}_{args.network}_{args.signal}"

    f = open(f"condor/{condorBase}/submit.jds", "w")
    f.write("universe = vanilla\n")
    f.write(f"executable = condor/{condorBase}/run.sh\n")
    f.write(f"jobbatchname = {jobbatchname}\n")
    f.write('+singularityimage = "/data6/Users/choij/Singularity/torch"\n')
    f.write("requirements = HasSingularity\n")
    f.write("request_cpus = 8\n")
    f.write("request_memory = 30 GB\n")
    f.write(f"log = condor/{condorBase}/job.log\n")
    f.write(f"output = condor/{condorBase}/job.out\n")
    f.write(f"error = condor/{condorBase}/job.err\n")
    f.write("queue 1")
    f.close()

def makeRunSh():
    # make run command
    command = f"python optimize.py --era {args.era} --channel {args.channel} --signal {args.signal} --network {args.network} --xsec {args.xsec}"

    f = open(f"condor/{condorBase}/run.sh", "w")
    f.write("#/bin/bash\n")
    f.write('export WORKDIR="/data6/Users/choij/ChargedHiggsAnalysis"\n')
    f.write('export PYTHONPATH="${PYTHONPATH}:${WORKDIR}"\n')
    f.write('export PYTHONPATH="${PYTHONPATH}:${WORKDIR}/libPython"\n')
    f.write("cd $WORKDIR/SignalRegionStudy\n")
    f.write("source /opt/conda/bin/activate\n")
    f.write("conda activate torch\n")
    f.write(f"{command}\n")
    f.close()

if __name__ == "__main__":
    os.makedirs(f"condor/{condorBase}")
    print(f"Running condor job in condor/{condorBase}...")
    makeSubmitJds()
    makeRunSh()
    os.chmod(f"condor/{condorBase}/run.sh", 0o755)
    os.system(f"condor_submit condor/{condorBase}/submit.jds")


