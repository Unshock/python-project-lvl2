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
            style == 'stylish':
        return str(value)
    return '"{}"'.format(str(value))


def make_tree_value(tree_value, depth=0, style='slylish', indent=4):
    result = '{\n'
    list_of_values = list(tree_value.items())
    for key, value in list_of_values:
        last_in_list = False if list_of_values.index((key, value)) < len(
            list_of_values) - 1 else True
        result += get_normalized_key(key, depth=depth, style=style,
                                     indent=indent)
        result += get_normalized_value(value, depth + 1, style=style,
                                       indent=indent)
        result += ',\n' if last_in_list is False and style == 'json' else '\n'
    result += '{}{}'.format(' ' * indent * (depth - 1), '}')
    result += ',' if last_in_list is False and style == 'json' else ''
    return result


def make_node(key, value, **kwargs):
    depth = kwargs['depth']
    status = kwargs['status']
    style = kwargs['style']
    indent = kwargs['indent']

    if status == 'updated':
        result = make_node(key, value[0], depth=depth,
                           status='deleted', style=style, indent=indent)
        result += ',\n' if style == 'json' else '\n'
        result += make_node(key, value[1], depth=depth, status='added',
                            style=style, indent=indent)
        return result
    result = get_normalized_key(key, status=status, depth=depth, style=style,
                                indent=indent)
    result += '{}'.format(
        get_normalized_value(value, depth + 1, style=style, indent=indent))
    return result


def make_result(node, depth, **kwargs):
    last_in_list = kwargs['last_in_list']
    style = kwargs['style']
    indent = kwargs['indent']

    result = make_node(node['name'], node['value'],
                       depth=depth, status=node['status'],
                       style=style, indent=indent)
    result += ',\n' if last_in_list is False and style == 'json' else '\n'
    return result


def make_diff(list_of_nodes_with_parameters, style='stylish', indent=4):
    def inner(list, depth=1, style='stylish', indent=4):
        result = ''
        for node in list:
            last_in_list = True if list.index(node) == len(list) - 1\
                or style == 'stylish' else False
            if node['status'] == 'updated, needs DFS':
                result += get_normalized_key(node['name'], depth=depth,
                                             style=style, indent=indent) + '{\n'
                result += inner(node['value'], depth + 1, style=style,
                                indent=indent)
                result += ' ' * indent * depth + '}'
                result += ',\n' if last_in_list is False else '\n'
            else:
                result += make_result(node, depth, last_in_list=last_in_list,
                                      style=style,
                                      indent=indent)
        return result
    result = inner(list_of_nodes_with_parameters, style=style, indent=indent)
    return '{}{}{}'.format('{\n', result, '}')
