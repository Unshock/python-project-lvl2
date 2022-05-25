import json
import yaml
from gendiff import generator
from gendiff.formatter import set_format


def load_file_by_path(file_path):
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        result = yaml.load(open(file_path), Loader=yaml.CLoader)
    elif file_path.endswith('.json'):
        result = json.load(open(file_path))
    return result


def generate_diff(file_path_1, file_path_2, formatter='stylish'):
    file_1 = load_file_by_path(file_path_1)
    file_2 = load_file_by_path(file_path_2)
    checking_list = generator.make_checking_list(file_1, file_2)
    diff = set_format(formatter)(checking_list)
    return diff

import pprint


file_1 = load_file_by_path('/home/victor/python/python-project-lvl2/tests/fixtures/file3.json')
file_2 = load_file_by_path('/home/victor/python/python-project-lvl2/tests/fixtures/file4.json')
pprint.pprint(generator.make_checking_list(file_1, file_2), indent=1)
