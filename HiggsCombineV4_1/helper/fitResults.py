fitParameters = {
    "2016preVFP": {
        "Skim1E2Mu": None,
        "Skim3Mu": (-0.014418862195814227,0.009497193922498263,3.4861534641970185e-05),
    },
    "2016postVFP": {
        "Skim1E2Mu": None,
        "Skim3Mu": (-0.017083164911061696,0.009758489908008282,3.0175553370784154e-05)
    },
    "2017": {
        "Skim1E2Mu": None,
        "Skim3Mu": (-0.015173996867449508,0.009518211662511348,2.9211344558189003e-05),
    },
    "2018": {
        "Skim1E2Mu": None,
        "Skim3Mu": (-0.010893444688277444,0.009350541655683772,3.3295935354653986e-05)
    }
}




def getFitSigmaValue(era: str, channel: str, mA: float):
    # check arguments
    if era not in ["2016preVFP", "2016postVFP", "2017", "2018"]:
        print(f"[getFitSigmaValue] Wrong era {era}")
        exit(1)
    if channel not in ["Skim1E2Mu", "Skim3Mu"]:
        print(f"[getFitSigmaValue] Wront channel {channel}")
        exit(1)

    a0, a1, a2 = fitParameters[era][channel]
    return a0 + a1*mA + a2*(mA**2)

if __name__ == "__main__":
    print(getFitSigmaValue("2018", "Skim3Mu", 30))
