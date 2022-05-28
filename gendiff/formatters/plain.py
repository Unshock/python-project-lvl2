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
    if isinstance(value, str):
        return f"'{value}'"
    return python_to_js[value] if value in python_to_js.keys() else value


def to_str(value):
    if isinstance(value, dict):
        return '[complex value]'
    return normalize_value(value)


def make_plain_diff(json_diff):
    diff = json.loads(json_diff)
    result = ''
    result += iter_(diff)
    return result


def iter_(json_diff):
    def inner(diff, path_name=""):
        children = diff.get("children")
        value = to_str(diff.get("value"))
        value1 = to_str(diff.get("value1"))
        value2 = to_str(diff.get("value2"))
        path_name = make_path(diff.get("key"), path_name)

        if diff["type"] == "root":
            lines = map(lambda child: inner(child), children)
            result = '\n'.join(lines)
            return f'{result}'

        if diff["type"] == "nested":
            lines = map(lambda child: inner(child, path_name=path_name),
                        children)
            lines = filter(lambda elem: elem != 'unchanged', lines)
            result = '\n'.join(lines)
            return result

        if diff["type"] == "added":
            return f'Property \'{path_name}\' was added with value: {value}'

        if diff["type"] == "deleted":
            return f'Property \'{path_name}\' was removed'

        if diff["type"] == "changed":
            return f'Property \'{path_name}\' was updated.' \
                   f' From {value1} to {value2}'

        if diff["type"] == "unchanged":
            return 'unchanged'

    return inner(json_diff)
