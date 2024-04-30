fitParameters = {
    "2016preVFP": {
        "Skim1E2Mu": (0.0025338576907751337,0.008503912234633017,3.7928349454765736e-05),
        "Skim3Mu": (-0.014822643551535286,0.009465341814629082,3.53377802499219e-05),
    },
    "2016postVFP": {
        "Skim1E2Mu": (0.006447340549575714,0.008038188517535553,3.9951953412688714e-05),
        "Skim3Mu": (-0.015300871387454944,0.009670450629877574,3.067796735273536e-05),
    },
    "2017": {
        "Skim1E2Mu": (-0.005273848438096251,0.008803307716954213,3.1809786432330966e-05),
        "Skim3Mu": (-0.01484509799691762,0.009474269961994849,3.0001560906853658e-05),
    },
    "2018": {
        "Skim1E2Mu": (0.001439036209024712,0.008482377497434891,3.405178803476662e-05),
        "Skim3Mu": (-0.01014389701713453,0.009310372030582973,3.35892011933559e-05)
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
    print(getFitSigmaValue("2017", "Skim3Mu", 30))
