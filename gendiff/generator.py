import json


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


def generate_diff(file_path_1, file_path_2):
    json_1 = json.load(open(file_path_1))
    json_2 = json.load(open(file_path_2))
    checking_list = make_checking_list(json_1, json_2)

    diff = "{"
    for elem in checking_list:
        diff += '\n  {} {}: {}'.format(elem['status'],
                                       elem['key'],
                                       elem['value'])
    diff += '\n}'

    return diff


@make_normalization
def make_checking_list(dict1, dict2):

    checking_list = []

    for key, value in dict1.items():

        if dict2.get(key) == value:
            element_dict = make_element_dict(key, value, source='dict_1')
            checking_list.append(element_dict.copy())

        else:
            element_dict = make_element_dict(key, value,
                                             source='dict_1', status='-')
            checking_list.append(element_dict.copy())

    for key, value in dict2.items():
        if dict1.get(key) != value:
            element_dict = make_element_dict(key, value,
                                             source='dict_2', status='+')
            checking_list.append(element_dict.copy())

    return checking_list
