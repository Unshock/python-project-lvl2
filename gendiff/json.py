def get_normalized_key(key, status='unchanged', depth=0):
    status_interpretation = {
        'unchanged': '',
        'deleted': '- ',
        'added': '+ ',
    }
    status = status_interpretation[status]
    result = '{}"{}{}": '.format(' ' * 2 * depth, status, key)
    return result


def get_normalized_value(value, depth):
    if isinstance(value, dict):
        return make_tree_value(value, depth)
    else:
        value = value if\
            not isinstance(value, str) or value in ['false', 'true', 'null']\
            else '"{}"'.format(value)
    return str(value)


def make_tree_value(tree_value, depth=0, last_in_list=False):
    result = '{\n'
    list_of_values = list(tree_value.items())
    for key, value in list_of_values:
        last_in_list = False if list_of_values.index((key, value)) < len(
            list_of_values) - 1 else True
        result += get_normalized_key(key, depth=depth)
        result += get_normalized_value(value, depth + 1)
        result += ',\n' if last_in_list is False else '\n'
    result += '{}{}'.format(' ' * 2 * (depth - 1), '}')
    result += ',' if last_in_list is False else ''
    return result


def make_node(key, value, depth=0, status='unchanged'):
    if status == 'updated':
        result = make_node(key, value[0], depth=depth,
                           status='deleted') + ',\n'
        result += make_node(key, value[1], depth=depth, status='added')
        return result
    result = get_normalized_key(key, status=status, depth=depth)
    result += '{}'.format(get_normalized_value(value, depth + 1))
    return result


def make_result(node, depth, last_in_list=False):
    result = make_node(node['name'], node['value'],
                       depth=depth, status=node['status'])
    result += ',\n' if last_in_list is False else '\n'
    return result


def make_json_diff(list_of_nodes_with_parameters):
    def inner(list, depth=1):
        json_diff1 = ''
        for node in list:
            last_in_list = True if list.index(node) == len(list) - 1 else False
            if node['status'] == 'updated, needs DFS':
                json_diff1 += get_normalized_key(node['name'],
                                                 depth=depth) + '{\n'
                json_diff1 += inner(node['value'], depth + 1)
                json_diff1 += ' ' * 2 * (depth) + '}'
                json_diff1 += ',\n' if last_in_list is False else '\n'
            else:
                json_diff1 += make_result(node, depth, last_in_list)
        return json_diff1
    result = inner(list_of_nodes_with_parameters)
    return '{}{}{}'.format('{\n', result, '}')
