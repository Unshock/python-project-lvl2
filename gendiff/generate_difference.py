import json
import yaml
from gendiff import generator
from gendiff.formatter import set_format


def load_file_by_path(file_path):
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        result = yaml.load(open(file_path), Loader=yaml.CLoader)
    elif file_path.endswith('.json'):
        result = json.load(open(file_path))
    else:
        raise Exception('File format is not supported')
    return result


def generate_diff(file_path_1, file_path_2, formatter='stylish'):
    file_1 = load_file_by_path(file_path_1)
    file_2 = load_file_by_path(file_path_2)
    json_diff = generator.build(file_1, file_2)
    if formatter == 'json':
        return json_diff
    styled_diff = set_format(formatter)(json_diff)
    return styled_diff
