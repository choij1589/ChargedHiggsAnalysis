import os, shutil
import argparse
import ROOT

WORKDIR = os.getenv("WORKDIR")
ROOT.gSystem.Load(f"{WORKDIR}/libCpp/hadd_cc.so")

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--signal", required=True, type=str, help="signal mass point")
parser.add_argument("--network", required=True, type=str, help="network")
parser.add_argument("--doCnC", action="store_true", default=False, help="do CnC or shape")
parser.add_argument("--doCut", action="store_true", default=False, help="use optimized score cuts?")
args = parser.parse_args()

# make a suffix
suffix = ".withcut.root" if args.doCut else ".nocut.root"
suffix = f".CnC{suffix}" if args.doCnC else f".shape{suffix}"

ROOT.hadd(args.era, args.channel, args.signal, args.network, suffix)
