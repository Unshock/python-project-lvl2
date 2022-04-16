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
        return str(value)


def make_checking_list(file_1, file_2):
    diff = []
    for key, value in file_1.items():
        value_file_1 = normalize_value(value)

        if key in file_2.keys():
            value_file_2 = normalize_value(file_2[key])

            if not isinstance(value_file_1, dict):
                if isinstance(value_file_2, dict):
                    diff.append({'name': key, 'status': 'updated',
                                 'value': (value_file_1, value_file_2)})
                else:
                    if value_file_1 == value_file_2:
                        diff.append({'name': key, 'status': 'unchanged',
                                     'value': value_file_1})
                    else:
                        diff.append({'name': key, 'status': 'updated',
                                     'value': (value_file_1, value_file_2)})
            else:
                if not isinstance(file_2[key], dict):
                    diff.append({'name': key, 'status': 'updated',
                                 'value': (value_file_1, value_file_2)})
                else:
                    diff.append(
                        {'name': key, 'status': 'updated, needs DFS',
                         'value': make_checking_list(value_file_1,
                                                     value_file_2)})
        else:
            diff.append(
                {'name': key, 'status': 'deleted', 'value': value_file_1})

    for key, value in file_2.items():
        value_file_2 = normalize_value(value)
        if key not in file_1.keys():
            diff.append({'name': key, 'status': 'added', 'value': value_file_2})

    diff.sort(key=lambda node: node['name'])
    return diff


def make_standardized_value(key, value, depth=0, status='unchanged'):
    initial_depth = depth

    def inner(key, value, depth=0, status='unchanged'):
        status_interpretation = {
            'unchanged': '    ',
            'deleted': '  - ',
            'added': '  + ',
        }
        status = status_interpretation[status]
        result = ''

        if not isinstance(value, dict):
            result += ('{}{}{}: {}{}'.format(' ' * 4 * depth, status, str(key),
                                             str(value), '\n'))
        else:
            result += (
                '{}{}{}{}'.format(' ' * 4 * depth, status, str(key), ': {\n'))
            for inner_key, inner_value in list(value.items()):
                if not isinstance(inner_value, dict):
                    result += ('{}{}: {}{}'.format(' ' * 4 * (depth + 2),
                                                   str(inner_key),
                                                   str(inner_value), '\n'))
                else:
                    result += inner(inner_key, inner_value, depth + 1)

            result += ('{}{}'.format(' ' * 4 * (depth + 1), '}'))
            result += '\n' if depth >= initial_depth else ''

        return result
    return inner(key, value, depth, status)


def make_node_visualization(node, depth=0):
    initial_depth = depth

    def inner(node, depth=0, result=''):
        if node['status'] == 'updated, needs DFS':
            result += "{}{}: {}".format(' ' * 4 * max(depth, depth + 1),
                                        node['name'], '{\n')
            for elem in node['value']:
                result += inner(elem, depth + 1)

            result += '{}{}'.format(' ' * 4 * max(depth, depth + 1), '}')
            result += '\n' if depth >= initial_depth else ''

        if node['status'] == 'updated':
            result += make_standardized_value(node['name'], node['value'][0],
                                              depth, status='deleted')
            result += make_standardized_value(node['name'], node['value'][1],
                                              depth, status='added')
            return result

        if node['status'] == 'deleted':
            result += make_standardized_value(node['name'], node['value'],
                                              depth, status='deleted')
            return result

        if node['status'] == 'added':
            result += make_standardized_value(node['name'], node['value'],
                                              depth, status='added')
            return result

        if node['status'] == 'unchanged':
            result += make_standardized_value(node['name'], node['value'],
                                              depth)
            return result

        return result
    return inner(node)


def make_stylish_diff(list_of_nodes):
    stylish_diff = '{\n'
    for elem in list_of_nodes:
        stylish_diff += make_node_visualization(elem)
    stylish_diff += '}'
    return stylish_diff
