import json
import os
import itertools
import copy
import subprocess

from optparse import OptionParser

#input_folder = 'C:/langevin_simulator-binding/x64/Release/'
#task_file_name = "cf2.json"
#parent_config_filename = 'cf1.json'
#results_folder = "C:/langevin_simulator-binding/x64/Release/results/"

def get_path_file(key, options):
    """Getting paths and the name of the configuration files, and the number of cores.

     Keyword arguments:
         key -- class 'str', argument name corresponding to path or file name / number of cores
         options -- class 'optparse.Values', contains the value of the argument

    """

    if not hasattr(options, key):
        raise ValueError(f"There is no {key} option")
    return getattr(options, key)


def run_simulator(configs, options):
    """ Launches simulator langevin_simulator-binding with passing arguments -paramsfile, -taskfile, -nthreads.

    Keyword arguments:
        configs -- class 'list', contains the names of the created configuration files
        options -- class 'optparse.Values', contains the value of the argument (-paramsfile, -taskfile, -nthreads).

    """

    nthreads = int(get_path_file("nthreads", options))
    exe_file = os.path.join(get_path_file("input_folder", options), 'langevin_simulator-binding.exe')
    paramsfile = ';'.join([os.path.join(get_path_file("results_folder", options), item) for item in configs])
    taskfile = os.path.join(get_path_file("input_folder", options), get_path_file("task_file_name", options))

    arg = f'{exe_file} -paramsfile {paramsfile} -taskfile {taskfile} -nthreads {nthreads - 1}'
    simulator = subprocess.call(arg)
    
    if not simulator:
        raise RuntimeError(f"simulator return exit code {simulator}")


def creation_configs(options):
    """Creates configuration files based on the parent configuration file and writes to them all possible
    combinations of parameter values from the job file. Returns a list with the names of the created files.

    Keyword arguments:
         options -- class 'optparse.Values', contains the value of the arguments corresponding to path or
         file name / number of cores.

    """

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
                config['Configuration']['Name'] = f'{numb_dict}_{numb_comb + 1}'
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

    configs = creation_configs(options)
    run_simulator(configs, options)