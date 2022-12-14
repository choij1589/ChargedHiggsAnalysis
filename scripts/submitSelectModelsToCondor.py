import os
import sys
import uuid
import argparse

# Sync arguments with triLepRegion/selectModels.py
parser = argparse.ArgumentParser()
parser.add_argument("--signal", "-s", required=True, type=str, help="Signal mass point")
parser.add_argument("--background", "-b", required=True, type=str, help="background")
args = parser.parse_args()

# make random string
process = uuid.uuid4().hex.upper()[:6]


def makeSubmitJds():
    f = open(f"condor/temp_{process}/submit.jds", "w")
    f.write(f"executable = condor/temp_{process}/run.sh\n")
    f.write('+singularityimage = "/data6/Users/choij/Singularity/torch"\n')
    f.write("requirements = HasSingularity\n")
    f.write("request_disk = 4 GB\n")
    f.write("request_memory = 4 GB\n")
    f.write("request_cpus = 4\n")
    f.write(f"log = condor/temp_{process}/job.log\n")
    f.write(f"output = condor/temp_{process}/job.out\n")
    f.write(f"error = condor/temp_{process}/job.err\n")
    f.write("queue 1")
    f.close()

def makeRunSh():
    f = open(f"condor/temp_{process}/run.sh", "w")
    f.write("#/bin/bash\n")
    f.write("echo $PWD\n")
    f.write('export WORKDIR="/data6/Users/choij/ChargedHiggsAnalysis"\n')
    f.write("cd $WORKDIR\n")
    f.write("source /opt/conda/bin/activate\n")
    f.write("conda activate torch\n")
    f.write(f"python triLepRegion/selectModels.py --signal {args.signal} --background {args.background}")
    f.close()

if __name__ == "__main__":
    os.makedirs(f"condor/temp_{process}")
    print(f"Running condor job in condor/temp_{process}...")
    makeSubmitJds()
    makeRunSh()
    os.chmod(f"condor/temp_{process}/run.sh", 0o755)
    os.system(f"condor_submit condor/temp_{process}/submit.jds")
