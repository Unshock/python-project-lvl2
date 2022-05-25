def make_simplified_value(value):
    if isinstance(value, str) and value not in ['false', 'true', 'null']:
        return "'{}'".format(value)
    return value if not isinstance(value, dict) else '[complex value]'


def make_plain_elem(element, path):
    path = "'{}'".format(path)
    if element['status'] == 'added':
        return "Property {} was added with value: {}"\
            .format(path, make_simplified_value(element['value']))
    elif element['status'] == 'deleted':
        return 'Property {} was removed'.format(path)
    return 'Property {} was updated. From {} to {}'.format(
        path, make_simplified_value(element['value'][0]),
        make_simplified_value(element['value'][1]))


def make_path(node, initial_path):
    return '.'.join((initial_path,
                     node['name'])) if initial_path != '' else node['name']


def make_plain_diff(list_of_nodes, path=''):
    initial_path = path
    result = []
    for node in list_of_nodes:
        path = make_path(node, initial_path)
        if isinstance(node['value'], list):
            result.append(make_plain_diff(node['value'], path))
        elif node['status'] != 'unchanged':
            result.append(make_plain_elem(node, path))
    result = '\n'.join(result)
    return result
