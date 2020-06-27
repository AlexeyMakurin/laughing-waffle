import json
import os
from optparse import OptionParser
import itertools
import copy

input_folder = "D:/Fazly/makurin/"
task_file_name = "cf2.json"
parent_config_filename = 'cf1.json'
results_folder = "D:/Fazly/makurin/results/"


def get_task_file(path):
    pass


def patch_config(cfg):
    pass


def main(args):
    with open(os.path.join(input_folder, task_file_name)) as f:
        templates = json.load(f)

    j = 0

    for cross_scan_dict in templates["Task"]["CrossScan"]:
        
        if cross_scan_dict != {}:
            j += 1

        type_params = [item.split("->") for item in cross_scan_dict]
        
        type_params_grouped = {key: [par[1] for par in group]
                     for key, group in itertools.groupby(type_params, lambda x: x[0])}

        cross_scan = [[cross_scan_dict[param_type + '->' + param] for param in params]
                      for param_type, params in type_params_grouped.items()]

        tmp_dict = dict(
            [(item, [dict(zip(type_params_grouped[item], comb)) for comb in itertools.product(*cross_scan[i])]) for item, i in
             zip(type_params_grouped, range(len(type_params_grouped)))])

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

        for key in type_params_grouped:
            new_config = [saves(item, key, path) for path in tmp_dict[key] for item in save_config]
            save_config = copy.deepcopy(new_config)

        for item, i in zip(new_config, range(len(new_config))):
            # print(i+1, item)
            with open(os.path.join(results_folder, f'conf_{j}_{i + 1}.json'), 'w') as f:
                json.dump(item, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    _, args = OptionParser().parse_args()
    print(_)
    print(args)
    
    main(args)

