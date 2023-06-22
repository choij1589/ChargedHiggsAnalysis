cuts = {
    # need update
    "2016preVFP": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.62,       # 45.31%
            "MHc-100_MA-95": 0.7,       # 53.37%
            "MHc-130_MA-90": 0.76,      # 70.74%
            "MHc-160_MA-85": 0.61,      # 46.99%
            "MHc-160_MA-120": 0.62,     # 39.85%
        }
    },
    "2016postVFP": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.69,       # 32.30%
            "MHc-100_MA-95": 0.73,      # 66.82%
            "MHc-130_MA-90": 0.69,      # 60.50%
            "MHc-160_MA-85": 0.74,      # 38.91%
            "MHc-160_MA-120": 0.74,     # 22.33%
        }
    },
    "2017": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.57,       # 50.62%
            "MHc-100_MA-95": 0.65,      # 55.09%
            "MHc-130_MA-90": 0.67,      # 55.28%
            "MHc-160_MA-85": 0.62,      # 34.14%
            "MHc-160_MA-120": 0.62,     # 39.68%
        }
    },
    "2018": {
        "Skim3Mu": {
            "MHc-70_MA-65": 0.73,       # 46.53%
            "MHc-100_MA-95": 0.62,      # 51.65%
            "MHc-130_MA-90": 0.72,      # 55.82%
            "MHc-160_MA-85": 0.57,      # 35.77%
            "MHc-160_MA-120": 0.54      # 30.87%
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

