import json
import os
import itertools
import copy
import subprocess
import shlex

from optparse import OptionParser

#input_folder = 'C:/langevin_simulator-binding/x64/Release/'
#task_file_name = "cf2.json"
#parent_config_filename = 'cf1.json'
#results_folder = "C:/langevin_simulator-binding/x64/Release/results/"

def get_path_file(key, options):
    if not hasattr(options, key):
        raise ValueError(f"There is no {key} option")
    return getattr(options, key)

def run_simulator(configs, options):

    nthreads = int(get_path_file("nthreads", options))
    exe_file = os.path.join(get_path_file("input_folder", options), 'langevin_simulator-binding.exe')
    taskfiles = ' '.join([os.path.join(get_path_file("results_folder", options), item) for item in configs])
    paramsfile = os.path.join(get_path_file("input_folder", options), get_path_file("task_file_name", options))

    arg = ' '.join([exe_file, f'-paramsfile {paramsfile}', f'-taskfile {taskfiles}', f'-nthreads {nthreads - 1}'])
    simulator = subprocess.call(arg)

    if simulator == 0:
        print('Success!')
    else:
        print('Error!')


def main(options):
    list_configs = []
    with open(os.path.join(get_path_file('input_folder', options), get_path_file('task_file_name', options))) as f:
        templates = json.load(f)

    numb_dict = 0
    for cross_scan_dict in templates["Task"]["CrossScan"]:
        if cross_scan_dict != {}:
            numb_dict += 1

            type_params = [item.split("->") for item in cross_scan_dict]
            type_params_grouped = {key: [par[1] for par in group]
                                   for key, group in itertools.groupby(type_params, lambda x: x[0])}
            
            combination_dict = dict()
            for type_param, params_list in type_params_grouped.items():
                # creation list values of parameters
                params_values_list = (cross_scan_dict[type_param + '->' + par] for par in params_list)

                # creation complex dict - {'type_parameter_i': [{'name_param_j': 'value'}]},
                # [] includes all combination for type_parameter_i
                combination_dict[type_param] = [dict(zip(params_list, comb)) for comb in itertools.product(*params_values_list)]

            with open(os.path.join(get_path_file('input_folder', options),
                                   get_path_file('parent_config_filename', options))) as f:
                configuration = json.load(f)

            save_configs = [configuration]

            def save(config, type_param, comb):
                config['Configuration'][type_param].update(comb)
                s = copy.deepcopy(config)
                return s

            # creation of configuration files based on the parent config
            for type_param, patch_list in combination_dict.items():
                new_configs = [save(config, type_param, comb) for comb in patch_list
                               for config in save_configs]
                save_configs = copy.deepcopy(new_configs)

            for numb_comb, config in enumerate(new_configs):
                with open(os.path.join(get_path_file('results_folder', options), f'conf_{numb_dict}_{numb_comb + 1}.json'), 'w')\
                        as f: json.dump(config, f, sort_keys=True, indent=2)
                list_configs.append(f'conf_{numb_dict}_{numb_comb + 1}.json')
    return list_configs

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option('-i', '--input_folder')
    parser.add_option('-t', '--task_file_name')
    parser.add_option('-p', '--parent_config_filename')
    parser.add_option('-r', '--results_folder')
    parser.add_option('-n', '--nthreads')

    (options, args) = parser.parse_args()

    configs = main(options)
    run_simulator(configs, options)