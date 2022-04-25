import json
import yaml


def load_file_by_path(file_path):
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        result = yaml.load(open(file_path), Loader=yaml.CLoader)
    elif file_path.endswith('json'):
        result = json.load(open(file_path))
    return result


def normalize_value(value):
    bool_normalization = {
        False: 'false',
        True: 'true',
        None: 'null',
    }
    if isinstance(value, dict):
        return value
    else:
        if value in bool_normalization:
            return bool_normalization[value]
        return value


def make_checking_list_elem(key, *args, status='undefined'):
    if status == 'undefined':
        status = get_status(args[0], args[1])

    if len(args) == 2 and status != 'unchanged':
        value = (args[0], args[1])
    else:
        value = args[0]

    if status == 'updated, needs DFS':
        value = make_checking_list(args[0], args[1])

    elem = {'name': key,
            'status': status,
            'value': value,
            }
    return elem


def get_status(value1, value2):
    if isinstance(value1, dict) and isinstance(value2, dict):
        return 'updated, needs DFS'
    if type(value1) != type(value2):
        return 'updated'
    else:
        return 'unchanged' if value1 == value2 else 'updated'


def make_checking_list(file_1, file_2):
    diff = []
    for key, value in file_1.items():
        value_file_1 = normalize_value(value)
        if key in file_2.keys():
            value_file_2 = normalize_value(file_2[key])
            diff.append(
                make_checking_list_elem(key, value_file_1, value_file_2))
        else:
            diff.append(
                make_checking_list_elem(key, value_file_1, status='deleted'))

    for key, value in file_2.items():
        value_file_2 = normalize_value(value)
        if key not in file_1.keys():
            diff.append(
                make_checking_list_elem(key, value_file_2, status='added'))

    diff.sort(key=lambda node: node['name'])
    return diff
