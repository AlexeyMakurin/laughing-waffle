import json
import itertools
import os
from optparse import OptionParser

input_folder = "D:/Fazly/makurin"
task_file_name = "cf2.json"
parent_config_filename = 'cf1.json'
results_folder = "D:/Fazly/makurin/results"


def get_task_file(path):
    pass


def patch_config(cfg):
    pass


def main():
    with open(os.path.join(input_folder, task_file_name)) as f:
        templates = json.load(f)

    for cross_scan_dict in templates["Task"]["CrossScan"]:

        model_params = [item.split("->") for item in cross_scan_dict]
        # model_params = [item.replace("ModelParameters->", "") for item in cross_scan_dict]

        keys = ...  # TODO

        cross_scan = list(cross_scan_dict.values())
        tmp_dict = [dict(zip(keys, comb)) for comb in itertools.product(*cross_scan)]

        with open(os.path.join(input_folder, parent_config_filename)) as f:
            configuration = json.load(f)

        model_parameters = configuration["Configuration"]["ModelParameters"]  # TODO fix last level

        for patch in tmp_dict:
            new_config = model_parameters.copy()
            new_config.update(patch)
            # TODO save new_config

        # for j in range(len(combination)):
        #     for param in model_parameters:
        #         for i in range(len(model_params)):
        #             if param == model_params[i]:
        #                 model_parameters[param] = combination[j][i]
        #     configuration["Configuration"]["ModelParameters"] = model_parameters

        # with open('conf_' + str(j + 1) + '.json', 'w') as f:
        #     json.dump(configuration, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    # main()
    _, args = OptionParser().parse_args()
    print(_)
    print(args)
