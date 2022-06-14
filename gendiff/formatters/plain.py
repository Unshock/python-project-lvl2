def render_plain(diff: dict) -> str:
    """
    :param diff: standard diff between two files in dict type
    :return: diff between two files in 'plain' format in string type
    """
    return iter_(diff)


def make_path(node_name: str, initial_path: str) -> str:
    """
    :param node_name: the name of node (the key) on the current depth
    :param initial_path: the name of node on the previous depth ('' if the
        previous depth was 0)
    :return: full name of node that is consisted of initial_path and current
        node name
    """
    return '.'.join((initial_path,
                     str(node_name))) if initial_path != '' else str(node_name)


def to_str(value):
    """
    :param value: node value in different types
    :return: value as required by the 'plain' formatter
    """
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if value is None:
        return 'null'
    if isinstance(value, str):
        return f"'{value}'"
    return value


def iter_(diff: dict) -> str:  # noqa: C901
    """
    :param diff: node of the diff between data of two files that has 'type' as
        a required key. Also, node could have 'children', 'key', one or two
        'values' depending on the type.
    :return: node in string type presented in 'plain' view
    """
    def inner(node, path_name=""):
        children = node.get("children")
        formatted_value = to_str(node.get("value"))
        formatted_value1 = to_str(node.get("value1"))
        formatted_value2 = to_str(node.get("value2"))
        path_name = make_path(node.get("key"), path_name)

        if node["type"] == "root":
            lines = map(lambda child: inner(child), children)
            result = '\n'.join(lines)
            return f'{result}'

        if node["type"] == "nested":
            lines = map(lambda child: inner(child, path_name=path_name),
                        children)
            lines = filter(lambda elem: elem != 'unchanged', lines)
            result = '\n'.join(lines)
            return result

        if node["type"] == "added":
            return f'Property \'{path_name}\' was added' \
                   f' with value: {formatted_value}'

        if node["type"] == "deleted":
            return f'Property \'{path_name}\' was removed'

        if node["type"] == "changed":
            return f'Property \'{path_name}\' was updated.' \
                   f' From {formatted_value1} to {formatted_value2}'

        return "unchanged"  # node type is 'unchanged'

    return inner(diff)
