from gendiff import tree_like_diff


def make_json_diff(list_of_nodes_with_parameters):
    return tree_like_diff.make_diff(list_of_nodes_with_parameters, style='json',
                                    indent=2)
