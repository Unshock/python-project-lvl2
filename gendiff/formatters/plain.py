import json


def make_path(node_name, initial_path):
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


def make_plain_diff(json_diff):
    diff = json.loads(json_diff)
    result = iter_(diff)
    return result


def make_added(path_name, value):
    return f'Property \'{path_name}\' was added with value: {value}'


def make_deleted(path_name):
    return f'Property \'{path_name}\' was removed'


def make_changed(path_name, value1, value2):
    return f'Property \'{path_name}\' was updated. From {value1} to {value2}'


def iter_(json_diff):
    def inner(diff, path_name=""):
        children = diff.get("children")
        value = to_str(diff.get("value"))
        value1 = to_str(diff.get("value1"))
        value2 = to_str(diff.get("value2"))
        path_name = make_path(diff.get("key"), path_name)

        line_builder = {
            'unchanged': 'unchanged',
            'added': make_added(path_name, value),
            'deleted': make_deleted(path_name),
            'changed': make_changed(path_name, value1, value2)
        }

        if diff["type"] == "root":
            lines = map(lambda child: inner(child), children)
            result = '\n'.join(lines)
            return f'{result}'

        elif diff["type"] == "nested":
            lines = map(lambda child: inner(child, path_name=path_name),
                        children)
            lines = filter(lambda elem: elem != 'unchanged', lines)
            result = '\n'.join(lines)
            return result

        else:
            return line_builder[diff["type"]]

    return inner(json_diff)
