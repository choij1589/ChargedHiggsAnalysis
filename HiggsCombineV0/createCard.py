import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--masspoint", required=True, type=str, help="masspoint")
args = parser.parse_args()

MA = int(args.masspoint.split("_")[1].split("-")[1])


promptSysts = ["L1Prefire", "PileupReweight", "MuonIDSF", "DblMuTrigSF", 
               "JetRes", "JetEn", "MuonEn", "ElectronEn", "ElectronRes"]


class DatacardManager():
    def __init__(self, era, channel, masspoint):
        self.csv = pd.read_csv(f"results/{era}/{channel}__/{masspoint}.csv", index_col="syst")
        self.backgrounds = []
        for bkg in ["nonprompt", "conversion", "diboson", "ttX", "others"]:
            # check evet rates are positive
            if self.get_event_rate(bkg) < 0: continue
            self.backgrounds.append(bkg)
            
    def get_event_rate(self, process, syst="Central"):
        if process == "signal":
            # scale signal rate to 5 fb
                return float(self.csv.loc[syst, process])*(1/3)
        else:
            return float(self.csv.loc[syst, process])
    
    def get_event_ratio(self, process, syst):
        return 1. + abs(self.get_event_rate(process, syst) / self.get_event_rate(process) - 1.)
    
    def add_systematics(self, syst):
        self.systematics.append(syst)
        
    def part1string(self):
        part1string = f"imax\t\t\t1 number of bins\n"
        part1string += f"jmax\t\t\t{len(self.backgrounds)} number of bins\n"
        part1string += f"kmax\t\t\t* number of nuisance parameters\n"
        part1string += "-"*120
        return part1string
    
    def part2string(self):
        observation = 0.
        for bkg in self.backgrounds: observation += self.get_event_rate(bkg)
        part2string = "bin\t\t\tsignal_region\n"
        part2string += f"observation\t\t{observation:.2f}\n"
        part2string += "-"*120
        return part2string
    
    def part3string(self):
        part3string = "bin\t\t\t" + "signal_region\t" * (len(self.backgrounds)+1) + "\n"
        
        part3string += "process\t\t\tAtoMuMu\t\t"
        for bkg in self.backgrounds: part3string += f"{bkg}\t"
        part3string += "\n"
        
        part3string += "process\t\t\t0\t\t"
        for idx in range(1, len(self.backgrounds)+1): part3string += f"{idx}\t\t"
        part3string += "\n"
        
        part3string += "rate\t\t\t"
        part3string += f"{self.get_event_rate('signal'):.2f}\t\t"
        for bkg in self.backgrounds:
            part3string += f"{self.get_event_rate(bkg):.2f}\t\t"
        part3string += "\n"
        part3string += "-"*120
        return part3string
    
    def syststring(self, syst, alias=None, type="lnN", value=None, skip=None):
        if alias is None: alias = syst
        syststring = f"{alias}\t{type}\t" 
        for process in ["signal"]+self.backgrounds:
            if process in skip: syststring += "-\t\t"
            elif value is None:
                ratio = max(self.get_event_ratio(process, f"{syst}Up"), self.get_event_ratio(process, f"{syst}Down"))
                syststring += f"{ratio:.3f}\t\t"
            else:
                syststring += f"{value:.3f}\t\t"
        return syststring

if __name__ == "__main__":
    manager = DatacardManager(args.era, args.channel, args.masspoint)
    print("# signal xsec scaled to be 5 fb")
    print(manager.part1string())
    print(manager.part2string())
    print(manager.part3string())
    print(manager.syststring(syst="lumi_13TeV", value=1.025, skip=["nonprompt", "conversion"]))
    for syst in promptSysts:
        print(manager.syststring(syst=syst, skip=["nonprompt", "conversion"]))
    print(manager.syststring(syst="Nonprompt", alias="nonprompt", skip=["signal", "conversion", "diboson", "ttX", "others"]))
    print(manager.syststring(syst="Conversion", alias="conversion", skip=["signal", "nonprompt", "diboson", "ttX", "others"]))
