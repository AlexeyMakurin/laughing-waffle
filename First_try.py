import json
import numpy as np

with open("cf2.json") as f:
   templates = json.load(f)

CrossScan = templates["Task"]["CrossScan"][0]

combination = []
Model_Params = []
Index = []

for item in CrossScan:
	Model_Params.append(item.replace("ModelParameters->", ""))
	Index.append(len(CrossScan[item]))
N = len(Model_Params)

def combs(i, param):
	combination.append(CrossScan["ModelParameters->" + param][i])


for index_0 in range(Index[0]):
	for index_1 in range(Index[1]):
		for index_2 in range(Index[2]):
			for index_3 in range(Index[3]):
				for index_4 in range(Index[4]):
					for index_5 in range(Index[5]):
						for index_6 in range(Index[6]):
							combs(index_0, "iniPhi")
							combs(index_1, "bindingDynamics")
							combs(index_2, "rotFriction")
							combs(index_3, "rotStiffness")
							combs(index_4, "Gdepth")
							combs(index_5, "movementTotalForce")
							combs(index_6, "rotWellDepth")

a = len(combination)
index = 0
json_data = np.ones((int(a/N),N))

while a - index != 0:
	for i in range(N):
		n = int(index/N)
		json_data[n][i] = combination[index + i]
	index = index + N;

with open("cf1.json") as f:
   configuration = json.load(f)

ModelParameters = configuration["Configuration"]["ModelParameters"]
 
for j in range(int(a/N)):
	for item in ModelParameters:
		for i in range(N):
			if item == Model_Params[i]:
				ModelParameters[item] = str(json_data[j][i])
	configuration["Configuration"]["ModelParameters"] = ModelParameters 

	with open('conf_' + str(j + 1) + '.json', 'w') as f:
		json.dump(configuration, f, sort_keys=True, indent=2)