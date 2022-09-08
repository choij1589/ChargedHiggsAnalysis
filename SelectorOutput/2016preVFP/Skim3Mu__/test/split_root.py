import argparse
from ROOT import TFile

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", required=True, type=str, help="Input root file")
parser.add_argument("--numbers", "-n", default=1, type=int, help="number of files to split")
args = parser.parse_args()

f = TFile.Open(args.input)
entries = f.Events.GetEntries()
split_range = []
for i in range(args.numbers):
    entry_size = (split_range - split_range%args.n) / 10
    split_range.append(i*entry_size)

for evt in f.Events:
    print(evt.GetEntry()

f.Close()

