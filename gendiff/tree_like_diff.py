def get_normalized_key(key, status='unchanged', **kwargs):
    depth = kwargs['depth']
    style = kwargs['style']
    indent = kwargs['indent']

    status_interpretation = {
        'unchanged': (indent - 2) * ' ' + ('' if style == 'json' else '  '),
        'deleted': (indent - 2) * ' ' + '- ',
        'added': (indent - 2) * ' ' + '+ ',
    }
    status = status_interpretation[status]
    result = '{}"{}{}": '.format(' ' * indent * depth, status, key)\
        if style == 'json'\
        else '{}{}{}: '.format(' ' * indent * (depth - 1), status, key)
    return result


def get_normalized_value(value, depth, style='slylish', indent=4):
    if isinstance(value, dict):
        return make_tree_value(value, depth, style=style, indent=indent)
    if not isinstance(value, str) or\
            value in ['false', 'true', 'null'] or\
            style != 'json':
        return str(value)
    return '"{}"'.format(str(value))


def put_comma(last_in_list=True, style='json'):
    return ',' if not last_in_list and style == 'json' else ''


def is_last_in_list(elem, list_):
    return False if list_.index(elem) < (len(list_) - 1) else True


def make_tree_value(tree_value, depth=0, style='slylish', indent=4):
    result = '{\n'
    list_of_values = list(tree_value.items())
    for key, value in list_of_values:
        last_in_list = is_last_in_list((key, value), list_of_values)
        result += get_normalized_key(key, depth=depth, style=style,
                                     indent=indent)
        result += get_normalized_value(value, depth + 1, style=style,
                                       indent=indent)
        result += put_comma(last_in_list=last_in_list, style=style) + '\n'
    result += '{}{}'.format(' ' * indent * (depth - 1), '}')
    result += put_comma(style=style)
    return result


def make_node(key, value, **kwargs):
    depth = kwargs['depth']
    status = kwargs['status']
    style = kwargs['style']
    indent = kwargs['indent']

    if status == 'updated':
        result = make_node(key, value[0], depth=depth,
                           status='deleted', style=style, indent=indent)
        result += put_comma(last_in_list=False, style=style) + '\n'
        result += make_node(key, value[1], depth=depth, status='added',
                            style=style, indent=indent)
        return result
    result = get_normalized_key(key, status=status, depth=depth, style=style,
                                indent=indent)
    result += '{}'.format(
        get_normalized_value(value, depth + 1, style=style, indent=indent))
    return result


def make_diff(list_of_nodes_with_parameters, depth=1, **kwargs):
    style = kwargs['style']
    indent = kwargs['indent']

    result = ''
    for node in list_of_nodes_with_parameters:
        last_in_list = is_last_in_list(node, list_of_nodes_with_parameters)
        if node['status'] == 'updated, needs DFS':
            result += get_normalized_key(node['name'], depth=depth,
                                         style=style, indent=indent) + '{\n'
            result += make_diff(node['value'], depth + 1, style=style,
                                indent=indent)
            result += ' ' * indent * depth + '}'
        else:
            result += make_node(node['name'], node['value'],
                                depth=depth, status=node['status'],
                                style=style, indent=indent)

        result += put_comma(last_in_list=last_in_list, style=style) + '\n'
    return result
