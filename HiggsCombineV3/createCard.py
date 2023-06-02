import ROOT as R
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--channel", required=True, type=str, help="channel")
parser.add_argument("--network", default="", type=str, help="network")
parser.add_argument("--masspoint", required=True, type=str, help="masspoint")
args = parser.parse_args()

MA = int(args.masspoint.split("_")[1].split("-")[1])


promptSysts = ["L1Prefire", "PileupReweight", "MuonIDSF", "DblMuTrigSF", 
               "JetRes", "JetEn", "MuonEn", "ElectronEn", "ElectronRes"]


class DatacardManager():
    def __init__(self, era, channel, network, masspoint):
        self.signal = masspoint
        if ("Net" in args.network): 
            self.rtfile = R.TFile.Open(f"results/{era}/{channel}__{network}__/{masspoint}/shapes_input.root")
        else:
            self.rtfile = R.TFile.Open(f"results/{era}/{channel}__/{masspoint}/shapes_input.root")
        self.backgrounds = []
        for bkg in ["nonprompt", "conversion", "diboson", "ttX", "others"]:
            # check if central event rates are positive
            h = self.rtfile.Get(bkg)
            if not h.Integral() > 0:
                print(f"# skip {bkg} for central event rate {h.Integral():.3f}")
                continue
            self.backgrounds.append(bkg)

    def get_event_rate(self, process, syst="Central"):
        if process == "data_obs":
            h = self.rtfile.Get("data_obs")
            return h.Integral()
        elif process == "signal":
            if syst == "Central": h = self.rtfile.Get(self.signal)
            else:                 h = self.rtfile.Get(f"{self.signal}_{syst}")
            return h.Integral()
        else:
            if syst == "Central": h = self.rtfile.Get(process)
            else:                 h = self.rtfile.Get(f"{process}_{syst}")
            return h.Integral()

    def get_event_stat(self, process, syst="Central"):
        #print(process, syst)
        if process == "signal":
            if syst == "Central": h = self.rtfile.Get(self.signal)
            else:                 h = self.rtfile.Get(f"{self.signal}_{syst}")
            return (h.GetMean(), h.GetStdDev())
        else:
            if syst == "Central": h = self.rtfile.Get(process)
            else:                 h = self.rtfile.Get(f"{process}_{syst}")
            return (h.GetMean(), h.GetStdDev())

    def get_event_ratio(self, process, syst):
        if syst == "stat":
            return 1. + self.get_event_rate(process, syst) / self.get_event_rate(process)
        else:
            return 1. + abs(self.get_event_rate(process, syst) / self.get_event_rate(process) - 1.)
    
    def part1string(self):
        part1string = f"imax\t\t1 number of bins\n"
        part1string += f"jmax\t\t{len(self.backgrounds)} number of bins\n"
        part1string += f"kmax\t\t* number of nuisance parameters\n"
        part1string += "-"*50
        return part1string
   
    def part2string(self):
        part2string = "shapes\t*\t*\tshapes_input.root\t$PROCESS\t$PROCESS_$SYSTEMATIC\n"
        part2string += f"shapes\tsignal\t*\tshapes_input.root\t{self.signal}\t{self.signal}_$SYSTEMATIC\n"
        part2string += "-"*50
        return part2string
    
    def part3string(self):
        part3string = "bin\t\t\tbin1\n"
        part3string = f"observation\t{self.get_event_rate('data_obs'):.4f}\n"
        part3string += "-"*50
        return part3string
   
    def part4string(self):
        part4string = "bin\t\t\t"
        part4string += "bin1\t\t" * (len(self.backgrounds)+1)
        part4string += "\n"
        part4string += f"process\t\t\tsignal\t\t"
        for bkg in self.backgrounds: 
            if len(bkg) < 8: part4string += f"{bkg}\t\t"
            else:            part4string += f"{bkg}\t"
        part4string += "\n"
        part4string += "process\t\t\t0\t\t"
        for iprocess in range(1, len(self.backgrounds)+1): part4string += f"{iprocess}\t\t"
        part4string += "\n"
        part4string += f"rate\t\t\t-1\t\t"
        part4string += "-1\t\t" * len(self.backgrounds)
        part4string += "\n"
        part4string += "-"*50
        return part4string

    def autoMCstring(self, threshold):
        return f"bin1\t\tautoMCStats\t{threshold}"

    def syststring(self, syst, alias=None, type=None, value=None, skip=None, denoteEra=False):
        if syst == "Nonprompt" and (not "nonprompt" in self.backgrounds): return ""
        if syst == "Conversion" and (not "conversion" in self.backgrounds): return ""

        # set alias
        if alias is None: alias = syst

        if denoteEra: alias = f"{alias}_{args.era}"
        
        # check type
        if type is None:
            # check every histogram input is not negative
            for process in ["signal"]+self.backgrounds:
                if process in skip: continue
                rate_up = self.get_event_rate(process, f"{syst}Up")
                rate_down = self.get_event_rate(process, f"{syst}Down")
                if not (rate_up >0. and rate_down > 0.): type = "lnN"

        if type != "lnN":
            for process in ["signal"]+self.backgrounds:
                if process in skip: continue
                mean, stddev = self.get_event_stat(process)
                mean_up, stddev_up = self.get_event_stat(process, f"{syst}Up")
                mean_down, stddev_down = self.get_event_stat(process, f"{syst}Down")
                
                # if mean & stddev within 0.5%, only vary normalization
                if stddev < 10e-6:                          continue
                if abs(mean - mean_up)/mean > 0.005:        type="shape"; break
                if abs(mean - mean_down)/mean > 0.005:      type="shape"; break
                if abs(stddev-stddev_up)/stddev > 0.005:    type="shape"; break
                if abs(stddev-stddev_down)/stddev > 0.005:  type="shape"; break
        
        if type != "shape": type = "lnN"

        if len(alias) < 8: syststring = f"{alias}\t\t{type}\t"
        else:              syststring = f"{alias}\t{type}\t"

        if type == "lnN":
            for process in ["signal"]+self.backgrounds:
                if process in skip: syststring += "-\t\t"
                elif value is None:
                    ratio = max(self.get_event_ratio(process, f"{syst}Up"), self.get_event_ratio(process, f"{syst}Down"))
                    syststring += f"{ratio:.3f}\t\t"
                else:
                    syststring += f"{value:.3f}\t\t"
        elif type == "shape":
            for process in ["signal"]+self.backgrounds:
                if process in skip: syststring += "-\t\t"
                else:               syststring += "1\t\t"
        else:
            print(f"what type is {type}?")
            raise(ValueError)

        return syststring


if __name__ == "__main__":
    manager = DatacardManager(args.era, args.channel, args.network, args.masspoint)
    print("# signal xsec scaled to be 5 fb")
    print(manager.part1string())
    print(manager.part2string())
    print(manager.part3string())
    print(manager.part4string())
    print(manager.autoMCstring(threshold=5))
    print(manager.syststring(syst="lumi_13TeV", type="lnN", value=1.025, skip=["nonprompt", "conversion"]))
    for syst in promptSysts:
        print(manager.syststring(syst=syst, skip=["nonprompt", "conversion"]))
    print(manager.syststring(syst="Nonprompt", skip=["signal", "conversion", "diboson", "ttX", "others"], denoteEra=True))
    print(manager.syststring(syst="Conversion", skip=["signal", "nonprompt", "diboson", "ttX", "others"]))
