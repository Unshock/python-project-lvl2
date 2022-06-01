def render_stylish(diff: dict) -> str:
    return iter_(diff)


def normalize_value(value):
    python_to_js = {
        False: "false",
        True: "true",
        None: "null",
    }
    if isinstance(value, bool) or value is None:
        return python_to_js[value]
    return value


def build_indent(depth: int) -> str:
    return (4 * depth + 2) * " "


def to_str(value1, depth: int):
    if isinstance(value1, dict):
        result = []
        for key, value in value1.items():
            result.append(f'{build_indent(depth + 1)}  {key}: '
                          f'{to_str(value, depth + 1)}')
        result = '\n'.join(result)
        return f"{{\n{result}\n{build_indent(depth)}  }}"
    return normalize_value(value1)


def make_unchanged(indent, key, value) -> str:
    return f"{indent}  {key}: {value}"


def make_added(indent, key, value) -> str:
    return f"{indent}+ {key}: {value}"


def make_deleted(indent, key, value) -> str:
    return f"{indent}- {key}: {value}"


def make_changed(indent, key, value1, value2) -> str:
    return f"{indent}- {key}: {value1}\n{indent}+ {key}: {value2}"


def iter_(node, depth=0) -> str:
    indent = build_indent(depth)
    children = node.get('children')
    key = node.get('key')
    formatted_value = to_str(node.get('value'), depth)
    formatted_value1 = to_str(node.get('value1'), depth)
    formatted_value2 = to_str(node.get('value2'), depth)

    line_builder = {
        'unchanged': make_unchanged(indent, key, formatted_value),
        'added': make_added(indent, key, formatted_value),
        'deleted': make_deleted(indent, key, formatted_value),
        'changed': make_changed(indent, key, formatted_value1, formatted_value2)
    }

    if node['type'] == 'root':
        lines = map(lambda child: iter_(child, depth), children)
        result = '\n'.join(lines)
        return f'{{\n{result}\n}}'

    elif node['type'] == 'nested':
        lines = map(lambda child: iter_(child, depth + 1), children)
        result = '\n'.join(lines)
        return f"{indent}  {key}: {{\n{result}\n{indent}  }}"

    return line_builder[node['type']]
