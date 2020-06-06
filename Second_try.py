import json
import itertools

with open("cf2.json") as f:
   templates = json.load(f)

CrossScan = templates["Task"]["CrossScan"][0]

Model_Params = []

for item in CrossScan:
	Model_Params.append(item.replace("ModelParameters->", ""))

cross_scan = list(CrossScan.values())
combination = list(itertools.product(*cross_scan))

n = len(Model_Params)
m = len(combination)

with open("cf1.json") as f:
   configuration = json.load(f)

ModelParameters = configuration["Configuration"]["ModelParameters"]

for j in range(m):
	for param in ModelParameters:
		for i in range(n):
			if param == Model_Params[i]:
				ModelParameters[param] = combination[j][i]
	configuration["Configuration"]["ModelParameters"] = ModelParameters 

	with open('conf_' + str(j + 1) + '.json', 'w') as f:
		json.dump(configuration, f, sort_keys=True, indent=2)
