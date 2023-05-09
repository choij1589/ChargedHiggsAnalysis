import os, shutil
import argparse
import pandas as pd
import ROOT
from pprint import pprint
WORKDIR = os.getenv("WORKDIR")
ROOT.gSystem.Load(f"{WORKDIR}/libCpp/fitAmass_cc.so")

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
args = parser.parse_args()

os.makedirs(f"{args.era}/{args.channel}__")

MASSPOINTs = ["MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
              "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
              "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
              "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"]

# prepare dictionary for dataframe
data = {}
data["masspoint"] = []
data["mA"] = []
data["mAErr"] = []
data["sigma"] = []
data["sigmaErr"] = []
data["width"] = []
data["widthErr"] = []

for masspoint in MASSPOINTs:
    print(f"fitting Amass for {masspoint}...")
    mA = float(masspoint.split("_")[1].split("-")[1])
    window = int(mA / 15)
    fitResult = ROOT.fitAmass(args.era, args.channel, masspoint, mA, mA-window, mA+window)
    mA = fitResult.at(0)
    sigma = fitResult.at(1)
    width = fitResult.at(2)
    data["masspoint"].append(masspoint)
    data["mA"].append(mA.getValV())
    data["mAErr"].append(mA.getError())
    data["sigma"].append(sigma.getValV())
    data["sigmaErr"].append(sigma.getError())
    data["width"].append(width.getValV())
    data["widthErr"].append(width.getError())

df = pd.DataFrame(data)
df.set_index("masspoint", inplace=True)
df.to_csv(f"{args.era}/{args.channel}__/fitResults.csv")
