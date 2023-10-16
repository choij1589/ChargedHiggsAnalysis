fitParameters = {
    "2016preVFP": {
        "Skim1E2Mu": (0.002051092235212111,0.00850198064536915,3.7697806664044333e-05),
        "Skim3Mu": (-0.014799351280331871,0.009462247644703187,3.5354427002960165e-05),
    },
    "2016postVFP": {
        "Skim1E2Mu": (0.0052202256104525585,0.008160315406445308,3.876310265750551e-05),
        "Skim3Mu": (-0.01549246329985568,0.009690892709113365,3.0496725448499714e-05),
    },
    "2017": {
        "Skim1E2Mu": (-0.005607958880653269,0.008829499095590228,3.145848293523468e-05),
        "Skim3Mu": (-0.014842506800501823,0.009474670293663456,2.9998726296491265e-05),
    },
    "2018": {
        "Skim1E2Mu": (0.002676537129180555,0.008412938882165565,3.483494827888128e-05),
        "Skim3Mu": (-0.0061755180247191795,0.009204582653635739,3.4207438641344634e-05)
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
