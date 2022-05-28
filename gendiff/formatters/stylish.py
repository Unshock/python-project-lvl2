import json


def make_stylish_diff(diff):
    diff = json.loads(diff)
    result = ''
    result += iter_(diff)
    return result


def normalize_value(value):
    python_to_js = {
        False: "false",
        True: "true",
        None: "null",
    }
    return python_to_js[value] if value in python_to_js.keys() else value


def build_indent(depth):
    return (4 * depth + 2) * " "


def to_str(value1, depth):
    if isinstance(value1, dict):
        result = []
        for key, value in value1.items():
            result.append(f'{build_indent(depth + 1)}  {key}: '
                          f'{to_str(value, depth + 1)}')
        result = '\n'.join(result)
        return f"{{\n{result}\n{build_indent(depth)}  }}"
    return normalize_value(value1)


def iter_(node, depth=0):  # noqa: C901
    children = node.get('children')
    indent = build_indent(depth)
    formatted_value = to_str(node.get('value'), depth)
    formatted_value1 = to_str(node.get('value1'), depth)
    formatted_value2 = to_str(node.get('value2'), depth)

    if node['type'] == 'root':
        lines = map(lambda child: iter_(child, depth), children)
        result = '\n'.join(lines)
        return f'{{\n{result}\n}}'

    elif node['type'] == 'nested':
        lines = map(lambda child: iter_(child, depth + 1), children)
        result = '\n'.join(lines)
        return f"{indent}  {node['key']}: {{\n{result}\n{indent}  }}"

    elif node['type'] == 'unchanged':
        return f"{indent}  {node['key']}: {formatted_value}"

    elif node['type'] == 'added':
        return f"{indent}+ {node['key']}: {formatted_value}"

    elif node['type'] == 'deleted':
        return f"{indent}- {node['key']}: {formatted_value}"

    elif node['type'] == 'changed':
        return f"{indent}- {node['key']}: {formatted_value1}\n" \
               f"{indent}+ {node['key']}: {formatted_value2}"
