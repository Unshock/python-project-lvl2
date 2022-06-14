def render_stylish(diff: dict) -> str:
    """
    :param diff: standard diff between two files in dict type
    :return: diff between two files in 'stylish' format in string type
    """
    return iter_(diff)


def build_indent(depth: int) -> str:
    """
    :param depth: depth of the node or value
    :return: the indent - a certain number of spaces - that is required for the
        'stylish' view and depends on the depth
    """
    return (4 * depth + 2) * " "


def to_str(value, depth: int):
    """
    :param value: node value in different types
    :param depth: node depth that is needed to build the indent if value is dict
    :return: value in json-like type and if value type is dict returns
        indented value
    """
    if isinstance(value, dict):
        result = []
        for key, dict_value in value.items():
            result.append(f'{build_indent(depth + 1)}  {key}: '
                          f'{to_str(dict_value, depth + 1)}')
        result = '\n'.join(result)
        return f"{{\n{result}\n{build_indent(depth)}  }}"

    if isinstance(value, bool):
        return 'true' if value else 'false'

    if value is None:
        return 'null'

    return value


def iter_(node, depth=0) -> str:
    """
    :param node: node of the diff between data of two files that has 'type' as
        a required key. Also, node could have 'children', 'key', one or two
        'values' depending on the type.
    :param depth: default depth is 0 and could be raised if node must be
        inspected deeper in recursive way
    :return: node in string type presented in 'stylish' view
    """
    indent = build_indent(depth)
    children = node.get('children')
    key = node.get('key')
    formatted_value = to_str(node.get('value'), depth)
    formatted_value1 = to_str(node.get('value1'), depth)
    formatted_value2 = to_str(node.get('value2'), depth)

    if node['type'] == 'root':
        lines = map(lambda child: iter_(child, depth), children)
        result = '\n'.join(lines)
        return f'{{\n{result}\n}}'

    if node['type'] == 'nested':
        lines = map(lambda child: iter_(child, depth + 1), children)
        result = '\n'.join(lines)
        return f"{indent}  {key}: {{\n{result}\n{indent}  }}"

    if node['type'] == 'changed':
        return f"{indent}- {key}: {formatted_value1}\n" \
               f"{indent}+ {key}: {formatted_value2}"

    if node['type'] == 'added':
        return f"{indent}+ {key}: {formatted_value}"

    if node['type'] == 'deleted':
        return f"{indent}- {key}: {formatted_value}"

    return f"{indent}  {key}: {formatted_value}"  # node type is 'unchanged'
