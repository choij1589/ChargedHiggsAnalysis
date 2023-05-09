import os
import sys
import uuid
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--network", required=True, type=str, help="network")
parser.add_argument("--sampleKey", required=True, type=str, help="sample list key")
parser.add_argument("--doCut", action="store_true", default=False, help="cut optimization")
parser.add_argument("--doCnC", action="store_true", default=False, help="CnC or shape analysis")
args = parser.parse_args()

# make random string
process = uuid.uuid4().hex.upper()[:6]
condorBase = f"prepareDatacard/{args.era}/{args.channel}__{args.network}__/{args.signal}/{args.sampleKey}"
condorBase = f"{condorBase}/CnC" if args.doCnC else f"{condorBase}/shape"
condorBase = f"{condorBase}__withcut" if args.doCut else f"{condorBase}__nocut"
condorBase = f"{condorBase}_{process}"

def makeSubmitJds():
    jobbatchname = f"prepareDatacard_{args.signal}_{args.sampleKey}"
    jobbatchname = f"{jobbatchname}_CnC" if args.doCnC else f"{jobbatchname}_shape"
    jobbatchname = f"{jobbatchname}_withcut" if args.doCut else f"{jobbatchname}_nocut"

    f = open(f"condor/{condorBase}/submit.jds", "w")
    f.write("universe = vanilla\n")
    f.write(f"executable = condor/{condorBase}/run.sh\n")
    f.write(f"jobbatchname = {jobbatchname}\n")
    f.write('+singularityimage = "/data6/Users/choij/Singularity/torch"\n')
    f.write("requirements = HasSingularity\n")
    f.write("request_cpus = 8\n")
    f.write("request_memory = 4 GB\n")
    f.write(f"log = condor/{condorBase}/job.log\n")
    f.write(f"output = condor/{condorBase}/job.out\n")
    f.write(f"error = condor/{condorBase}/job.err\n")
    f.write("queue 1")
    f.close()

def makeRunSh():
    # make run command
    command = f"python prepareDatacard.py --era {args.era} --channel {args.channel} --signal {args.signal} --network {args.network} --sampleKey {args.sampleKey}"
    if args.doCnC: command = f"{command} --doCnC"
    if args.doCut: command = f"{command} --doCut"

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
