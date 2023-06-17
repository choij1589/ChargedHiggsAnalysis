cuts = {
    "2016preVFP": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.51,       # 33.13%
            "MHc-100_MA-95": 0.75,      # 43.37%
            "MHc-130_MA-90": 0.58,      # 43.14%
            "MHc-160_MA-85": 0.69,      # 40.12%
            "MHc-160_MA-120": 0.57,     # 46.07%
        }
    },
    "2016postVFP": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.71,       # 72.52%
            "MHc-100_MA-95": 0.75,      # 40.88%
            "MHc-130_MA-90": 0.69,      # 44.5%
            "MHc-160_MA-85": 0.56,      # 38.05%
            "MHc-160_MA-120": 0.83,     # 75.49%
        }
    },
    "2017": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.76,       # 53.38%
            "MHc-100_MA-95": 0.65,      # 48.02%
            "MHc-130_MA-90": 0.64,      # 41.51%
            "MHc-160_MA-85": 0.7,       # 36.7%
            "MHc-160_MA-120": 0.81,     # 100.68%
        }
    },
    "2018": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.6,        # 46.32%
            "MHc-100_MA-95": 0.77,      # 47.51%
            "MHc-130_MA-90": 0.58,      # 36.16%
            "MHc-160_MA-85": 0.71,      # 28.58%
            "MHc-160_MA-120": 0.63      # 40.02%
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

