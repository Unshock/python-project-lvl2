import json
import yaml


def sort_checking_list(checking_list):
    return checking_list['key'], checking_list['source']


def make_normalization(function):
    bool_normalization_dict = {
        False: 'false',
        True: 'true',
        None: 'null',
    }

    def inner(*args, **kwargs):
        result = function(*args, **kwargs)
        result.sort(key=sort_checking_list)
        for elem in result:
            if elem['value'] in bool_normalization_dict:
                elem['value'] = bool_normalization_dict[elem['value']]
        return result
    return inner


def make_element_dict(key, value, source=None, status=' '):
    element_dict = {}

    element_dict['key'] = key
    element_dict['value'] = value
    element_dict['source'] = source
    element_dict['status'] = status

    return element_dict


def load_file_by_path(file_path):
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        result = yaml.load(open(file_path), Loader=yaml.CLoader)
    elif file_path.endswith('json'):
        result = json.load(open(file_path))

    return result


@make_normalization
def make_checking_list(dict1, dict2):

    checking_list = []

    for key, value in dict1.items():

        if dict2.get(key) == value:
            element_dict = make_element_dict(key, value, source='file_1')
            checking_list.append(element_dict.copy())

        else:
            element_dict = make_element_dict(key, value,
                                             source='file_1', status='-')
            checking_list.append(element_dict.copy())

    for key, value in dict2.items():
        if dict1.get(key) != value:
            element_dict = make_element_dict(key, value,
                                             source='file_2', status='+')
            checking_list.append(element_dict.copy())

    return checking_list


def make_formatted_diff(checking_list):
    diff = "{"
    for elem in checking_list:
        diff += '\n  {} {}: {}'.format(elem['status'],
                                       elem['key'],
                                       elem['value'])
    diff += '\n}'
    return diff
