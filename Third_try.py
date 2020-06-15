import json
import os
from optparse import OptionParser
import itertools 
import copy


input_folder = "C:/langevin_simulator-binding/x64/Release/"
task_file_name = "cf2.json"
parent_config_filename = 'cf1.json'
results_folder = "C:/langevin_simulator-binding/x64/Release/results/"


def get_task_file(path):
    pass

def patch_config(cfg):
    pass

def main():

    with open(os.path.join(input_folder, task_file_name)) as f:
	templates = json.load(f)
	
    j = 0

    for cross_scan_dict in templates["Task"]["CrossScan"]:
		
        if cross_scan_dict != {}:
	
	    j = j + 1
			
	    type_params = [item.split("->") for item in cross_scan_dict]

	    keys = dict([(key, [par[1] for par in group]) for key, group in itertools.groupby(type_params, lambda x: x[0])])

	    cross_scan = list([cross_scan_dict.get(item + '->' + key) for key in keys[item]] for item in keys)

	    tmp_dict = dict([(item,[dict(zip(keys[item], comb)) for comb in itertools.product(*cross_scan[i])]) for item, i in zip(keys, range(len(keys)))])

	    with open(os.path.join(input_folder, parent_config_filename)) as f:
		configuration = json.load(f)

	    model_parameters = configuration

	    config = model_parameters.copy()
	    save_config = model_parameters.copy()

	    def saves(item, key, path):
	        try:
		    config.update(save_config)
		except:
		    config.update(item)

		config['Configuration'][key].update(path)
		s = copy.deepcopy(config)
		return s

	    for key in keys:
	        new_config = [saves(item, key, path) for path in tmp_dict[key] for item in save_config] 
		save_config = copy.deepcopy(new_config)

	    for item, i in zip(new_config, range(len(new_config))):	
	        #print(i+1, item)
		with open(os.path.join(results_folder,'conf_' + str(j) + '_' + str(i + 1) + '.json'), 'w') as f:
		    json.dump(item, f, sort_keys=True, indent=2)

if __name__ == '__main__':
    main()
    _, args = OptionParser().parse_args()
    print(_)
    print(args)
