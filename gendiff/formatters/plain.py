def render_plain(diff: dict) -> str:
    return iter_(diff)


def make_path(node_name: str, initial_path: str) -> str:
    return '.'.join((initial_path,
                     str(node_name))) if initial_path != '' else str(node_name)


def normalize_value(value):
    python_to_js = {
        False: "false",
        True: "true",
        None: "null",
    }
    if isinstance(value, bool) or value is None:
        return python_to_js[value]
    return f"'{value}'" if isinstance(value, str) else value


def to_str(value):
    if isinstance(value, dict):
        return '[complex value]'
    return normalize_value(value)


def make_added(path_name, value) -> str:
    return f'Property \'{path_name}\' was added with value: {value}'


def make_deleted(path_name) -> str:
    return f'Property \'{path_name}\' was removed'


def make_changed(path_name, value1, value2) -> str:
    return f'Property \'{path_name}\' was updated. From {value1} to {value2}'


def iter_(diff: dict) -> str:
    def inner(node, path_name=""):
        children = node.get("children")
        formatted_value = to_str(node.get("value"))
        formatted_value1 = to_str(node.get("value1"))
        formatted_value2 = to_str(node.get("value2"))
        path_name = make_path(node.get("key"), path_name)

        line_builder = {
            'unchanged': 'unchanged',
            'added': make_added(path_name, formatted_value),
            'deleted': make_deleted(path_name),
            'changed': make_changed(path_name,
                                    formatted_value1, formatted_value2)
        }

        if node["type"] == "root":
            lines = map(lambda child: inner(child), children)
            result = '\n'.join(lines)
            return f'{result}'

        elif node["type"] == "nested":
            lines = map(lambda child: inner(child, path_name=path_name),
                        children)
            lines = filter(lambda elem: elem != 'unchanged', lines)
            result = '\n'.join(lines)
            return result

        else:
            return line_builder[node["type"]]

    return inner(diff)
