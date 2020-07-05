import json
import os
import itertools
import copy

from optparse import OptionParser

#input_folder = 'C:/langevin_simulator-binding/x64/Release/'
#task_file_name = "cf2.json"
#parent_config_filename = 'cf1.json'
#results_folder = "C:/langevin_simulator-binding/x64/Release/results/"


def get_path_file(key):
    for k, v in options.__dict__.items():
        if k == key:
            return v


def main():

    with open(os.path.join(get_path_file('input_folder'), get_path_file('task_file_name'))) as f:
        templates = json.load(f)

    numb_dict = 0

    for cross_scan_dict in templates["Task"]["CrossScan"]:

        if cross_scan_dict != {}:

            numb_dict += 1

            type_params = [item.split("->") for item in cross_scan_dict]
            type_params_grouped = {key: [par[1] for par in group]
                                   for key, group in itertools.groupby(type_params, lambda x: x[0])}

            # creation list values of parameters
            cross_scan = [[cross_scan_dict[type_param + '->' + par] for par in type_params_grouped[type_param]]
                          for type_param in type_params_grouped]
            # creation complex dict - {'type_parameter_i': [{'name_param_j': 'value'}]},
            # [] includes all combination for type_parameter_i
            combination_dict = {type_par: [dict(zip(par, comb)) for comb in itertools.product(*list_values)]
                                for (type_par, par), list_values in zip(type_params_grouped.items(), cross_scan)}

            with open(os.path.join(get_path_file('input_folder'), get_path_file('parent_config_filename'))) as f:
                configuration = json.load(f)

            save_configs = [configuration]

            def save(config, type_param, comb):
                config['Configuration'][type_param].update(comb)
                s = copy.deepcopy(config)
                return s

            #creation of configuration files based on the parent config
            for type_param in combination_dict.keys():
                new_configs = [save(config, type_param, comb) for comb in combination_dict[type_param]
                               for config in save_configs]
                save_configs = copy.deepcopy(new_configs)

            for config, numb_comb in zip(new_configs, range(len(new_configs))):
                with open(os.path.join(get_path_file('results_folder'), f'conf_{numb_dict}_{numb_comb + 1}.json'), 'w')\
                        as f: json.dump(config, f, sort_keys=True, indent=2)

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option('-i', '--input_folder')
    parser.add_option('-t', '--task_file_name')
    parser.add_option('-p', '--parent_config_filename')
    parser.add_option('-r', '--results_folder')

    (options, args) = parser.parse_args()

    main()

