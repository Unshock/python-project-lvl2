from gendiff import tree_like_diff


def make_json_diff(list_of_nodes_with_parameters, indent=2):
    result = tree_like_diff.make_diff(list_of_nodes_with_parameters,
                                      style='json', indent=indent)
    return '{}{}{}{}'.format('{', tree_like_diff.make_line_break(indent=indent),
                             result, '}')
