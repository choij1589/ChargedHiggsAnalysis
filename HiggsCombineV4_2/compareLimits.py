import json

comparison = "exp0"


path_default = "../HiggsCombineV4/limits/limits.2018.Skim3Mu.HybridNew.Shape.json"
path_alter = "limits/limits.2018.Skim3Mu.HybridNew.Shape.json"

with open(path_default, "r") as f:
    json_default = json.load(f)
with open(path_alter, "r") as f:
    json_alter = json.load(f)

limits_default = {}
limits_alter = {}
for key, value in json_default.items():
    limits_default[key] = value[comparison]

for key, value in json_alter.items():
    limits_alter[key] = value[comparison]


ratio = {}
for key in limits_default.keys():
    ratio[key] = (limits_alter[key] - limits_default[key]) / limits_default[key]
print(ratio)
