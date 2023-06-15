cuts = {
    "2016preVFP": {
        "Skim3Mu": {
            "MHc-70_MA-65": None,
            "MHc-100_MA-95": None,
            "MHc-130_MA-90": None,
            "MHc-160_MA-85": None,
            "MHc-160_MA-120": None,
        }
    },
    "2016postVFP": {
        "Skim3Mu": {
            "MHc-70_MA-65": None,
            "MHc-100_MA-95": None,
            "MHc-130_MA-90": None,
            "MHc-160_MA-85": None,
            "MHc-160_MA-120": None,
        }
    },
    "2017": {
        "Skim3Mu": {
            "MHc-70_MA-65": None,
            "MHc-100_MA-95": None,
            "MHc-130_MA-90": None,
            "MHc-160_MA-85": None,
            "MHc-160_MA-120": None,
        }
    },
    "2018": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.61,
            "MHc-100_MA-95": 0.77,
            "MHc-130_MA-90": 0.58,
            "MHc-160_MA-85": 0.54,
            "MHc-160_MA-120": 0.63
        }
    }
}

def parseMLCut(era: str, channel: str, signal: str):
    if era not in ["2016preVFP", "2016postVFP", "2017", "2018"]:
        print(f"[parseMLCuts] Wrong era {era}")
        exit(1)
    if channel not in ["Skim1E2Mu", "Skim3Mu"]:
        print(f"[parseMLCuts] Wrong channel {channel}")
        exit(1)

    return cuts[era][channel][signal]

