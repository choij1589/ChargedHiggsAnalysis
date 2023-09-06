from math import pow, sqrt
import argparse
import ROOT
ROOT.gSystem.Load("fitFunction_C.so")

parser = argparse.ArgumentParser()
parser.add_argument("--era", required=True, type=str, help="era")
parser.add_argument("--hlt", required=True, type=str, help="hlt path")
parser.add_argument("--id", required=True, type=str, help="loose or tight")
args = parser.parse_args()

ERA = args.era
HLT = args.hlt
ID =  args.id

#### Systematics
SYSTs = [["Central"]]
if "MeasFakeEl" in HLT:
    SYSTs.append(["PileupReweight"])
    SYSTs.append(["L1PrefireUp", "L1PrefireDown"])
    SYSTs.append(["ElectronRecoSFUp", "ElectronRecoSFDown"])
    SYSTs.append(["HeavyTagUpUnCorr", "HeavyTagDownUnCorr"])
    SYSTs.append(["LightTagUpUnCorr", "LightTagDownUnCorr"])
    SYSTs.append(["JetResUp", "JetResDown"])
    SYSTs.append(["JetEnUp", "JetEnDown"])
    SYSTs.append(["ElectronResUp", "ElectronResDown"])
    SYSTs.append(["ElectronEnUp", "ElectronEnDown"])
    SYSTs.append(["MuonEnUp", "MuonEnDown"])
if "MeasFakeMu" in HLT:
    SYSTs.append(["PileupReweight"])
    SYSTs.append(["L1PrefireUp", "L1PrefireDown"])
    SYSTs.append(["MuonRecoSFUp", "MuonRecoSFDown"])
    SYSTs.append(["HeavyTagUpUnCorr", "HeavyTagDownUnCorr"])
    SYSTs.append(["LightTagUpUnCorr", "LightTagDownUnCorr"])
    SYSTs.append(["JetResUp", "JetResDown"])
    SYSTs.append(["JetEnUp", "JetEnDown"])
    SYSTs.append(["ElectronResUp", "ElectronResDown"])
    SYSTs.append(["ElectronEnUp", "ElectronEnDown"])
    SYSTs.append(["MuonEnUp", "MuonEnDown"])


def get_prompt_ratio(syst="Central"):
    fitResult = ROOT.fitMT(ERA, HLT, ID, syst)
    out = fitResult.floatParsFinal()

    value = 0.
    error = 0.
    for i in range(out.getSize()):
        coef = out.at(i)
        this_value, this_error = coef.getVal(), coef.getError()
        value += this_value
        error += pow(this_error, 2)
    error = sqrt(error)
    return (value, error)

def eval_total_unc(valueDict, errorDict):
    value = valueDict["Central"]
    stat  = errorDict["Central"]
    totalUnc = pow(stat, 2)
    for syst in SYSTs:
        if len(syst) == 1:
            this_value = valueDict[syst[0]]
            this_error = errorDict[syst[0]]
            totalUnc += pow(this_value - value, 2)
        elif len(syst) == 2:
            syst_up, syst_down = tuple(syst)
            value_up, error_up = valueDict[syst_up], errorDict[syst_up]
            value_down, error_down = valueDict[syst_down], errorDict[syst_down]
            thisUnc = max(abs(value_up-value), abs(value_down-value))
            totalUnc += pow(thisUnc, 2)
        else:
            print(syst)
            continue
    return (value, stat, sqrt(totalUnc))

values = {}
errors = {}
for syst in SYSTs:
    if len(syst) == 1:
        this_value, this_error = get_prompt_ratio(syst[0])
        values[syst[0]] = this_value
        errors[syst[0]] = this_error
    elif len(syst) == 2:
        syst_up, syst_down = tuple(syst)
        value_up, error_up = get_prompt_ratio(syst_up)
        value_down, error_down = get_prompt_ratio(syst_down)
        values[syst_up] = value_up
        values[syst_down] = value_down
        errors[syst_up] = error_up
        errors[syst_down] = error_down
    else:
        print(syst)
        continue

value, stat, total = eval_total_unc(values, errors)

f = open(f"results/{ERA}/CSV/{HLT}_{ID}.csv", "w")
f.write("# syst, prompt_ratio, error\n")
for syst in values.keys():
    f.write(f"{syst}, {values[syst]}, {errors[syst]}\n")
f.write(f"total error = {total}({total/value*100:.2f}%)\n")
f.close()



