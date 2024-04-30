cuts = {
    # need update
    "2016preVFP": {
        "Skim1E2Mu": {
            "MHc-100_MA-95": 0.74,      # 48.23%
            "MHc-130_MA-90": 0.83,      # 73.61%
            "MHc-160_MA-85": 0.64,      # 46.13%
        },
        "Skim3Mu": {
            "MHc-100_MA-95": 0.65,      # 50.69%
            "MHc-130_MA-90": 0.80,      # 55.28%
            "MHc-160_MA-85": 0.56,      # 39.73%
        }
    },
    "2016postVFP": {
        "Skim1E2Mu": {
            "MHc-100_MA-95": 0.79,      # 43.82%
            "MHc-130_MA-90": 0.75,      # 74.27%
            "MHc-160_MA-85": 0.77,      # 61.63%
        },
        "Skim3Mu": {
            "MHc-100_MA-95": 0.7,       # 58.48%
            "MHc-130_MA-90": 0.72,      # 54.16%
            "MHc-160_MA-85": 0.69,      # 52.21%
        }
    },
    "2017": {
        "Skim1E2Mu": {
            "MHc-100_MA-95": 0.67,      # 38.71%
            "MHc-130_MA-90": 0.77,      # 72.44%
            "MHc-160_MA-85": 0.77,      # 45.02% 
        },
        "Skim3Mu": {
            "MHc-100_MA-95": 0.8,       # 52.27%
            "MHc-130_MA-90": 0.65,      # 46.99%
            "MHc-160_MA-85": 0.63,      # 34.04%
        }
    },
    "2018": {
        "Skim1E2Mu": {
            "MHc-100_MA-95": 0.74,      # 47.21%
            "MHc-130_MA-90": 0.8,       # 74.02%
            "MHc-160_MA-85": 0.7,       # 46.99%
        },
        "Skim3Mu": {
            "MHc-100_MA-95": 0.6,       # 44.35%
            "MHc-130_MA-90": 0.68,      # 49.16%
            "MHc-160_MA-85": 0.65,      # 42.88%
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

