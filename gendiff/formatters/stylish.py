from gendiff import tree_like_diff


def make_stylish_diff(list_of_nodes_with_parameters):
    result = tree_like_diff.make_diff(list_of_nodes_with_parameters,
                                      style='stylish', indent=4)
    return '{}{}{}'.format('{\n', result, '}')
