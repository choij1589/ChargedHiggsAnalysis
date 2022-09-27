import os
import sys
sys.path.insert(0, os.environ['WORKDIR'])
import subprocess
import uuid
import argparse
from time import sleep
from MetaInfo.periodInfo import PeriodDict

# Sync arguments with triLepRegion/makeMCHistograms.py
parser = argparse.ArgumentParser()
parser.add_argument("--era", "-e", required=True, type=str, help="era")
parser.add_argument("--sample", "-s", default="DYJets", type=str, help="sample name")
args = parser.parse_args()
periodList = PeriodDict[args.era]

# make random string
process = uuid.uuid4().hex.upper()[:6]

def makeSubmitJds(queue):
    f = open(f"condor/temp_{process}/submit.jds", "w")
    f.write(f"executable = condor/temp_{process}/run.sh\n")
    f.write(f"arguments = {args.sample}_$(ProcId)\n")
    f.write('+singularityimage = "/data6/Users/choij/Singularity/torch"\n')
    f.write("requirements = HasSingularity\n")
    f.write("request_memory = 4 GB\n")
    f.write(f"log = condor/temp_{process}/job_$(ProcId).log\n")
    f.write(f"output = condor/temp_{process}/job_$(ProcId).out\n")
    f.write(f"error = condor/temp_{process}/job_$(ProcId).err\n")
    f.write(f"queue {queue}")
    f.close()

def makeRunSh():
    f = open(f"condor/temp_{process}/run.sh", "w")
    f.write("#/bin/bash\n")
    f.write("SAMPLE=$1\n")
    f.write('export WORKDIR="/data6/Users/choij/ChargedHiggsAnalysis"\n')
    f.write("cd $WORKDIR\n")
    f.write("source /opt/conda/bin/activate\n")
    f.write("conda activate torch\n")
    f.write(f"python triLepRegion/makeDataHistograms.py --era {args.era} --sample $SAMPLE")
    f.close()

def isJobStatusDone(clusterID):
    result = subprocess.run(f"condor_q {clusterID}".split(),
                            capture_output=True,
                            encoding="utf-8")
    isDone = clusterID not in result.stdout
    return isDone

if __name__ == "__main__":
    os.makedirs(f"condor/temp_{process}")
    print(f"Running condor job in condor/temp_{process}...")
    # decide the number of procs to submit
    makeSubmitJds(len(periodList))
    makeRunSh()
    os.chmod(f"condor/temp_{process}/run.sh", 0o755)
    result = subprocess.run(f"condor_submit condor/temp_{process}/submit.jds".split(),
                            capture_output=True,
                            encoding="utf-8")
    result = result.stdout.split("\n")[-2]
    clusterID = result.split(" ")[-1][:-1]

    # check whether the job has been done
    while True:
        if isJobStatusDone(clusterID):
            print(f"condor job {clusterID} has been done")
            break
        else:
            sleep(1)
    
    # now hadd the outputs
    basedir = f"triLepRegion/ROOT/Skim3Mu__/{args.era}"
    os.system(f"hadd -f {basedir}/{args.sample}.root {basedir}/{args.sample}_*.root")
    #for period in periodList:
    #    os.remove(f"{basedir}/{args.sample}_{period}.root")

