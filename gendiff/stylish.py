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


def add_standardized_value(node, depth, status):
    result = ''
    if status == 'updated':
        result += make_standardized_value(node['name'], node['value'][0],
                                          depth, status='deleted')
        result += make_standardized_value(node['name'], node['value'][1],
                                          depth, status='added')
    else:
        result += make_standardized_value(node['name'], node['value'],
                                          depth, status)
    return result


def make_node_visualization(node, depth=0):
    initial_depth = depth

    def inner(node, depth=0, result=''):
        current_node_status = node['status']
        if current_node_status == 'updated, needs DFS':
            result += "{}{}: {}".format(' ' * 4 * max(depth, depth + 1),
                                        node['name'], '{\n')
            for elem in node['value']:
                result += inner(elem, depth + 1)

            result += '{}{}'.format(' ' * 4 * max(depth, depth + 1), '}')
            result += '\n' if depth >= initial_depth else ''
        else:
            result = add_standardized_value(node, depth, current_node_status)
        return result
    return inner(node)


def make_stylish_diff(list_of_nodes):
    stylish_diff = '{\n'
    for elem in list_of_nodes:
        stylish_diff += make_node_visualization(elem)
    stylish_diff += '}'
    return stylish_diff
