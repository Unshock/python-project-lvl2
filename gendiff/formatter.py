from gendiff.formatters import plain, stylish, json


def formatting(diff: dict, formatter: str) -> str:
    """
    :param diff: difference between first file data and second file data as dict
     where 'type' is 'root' and 'children' is the list of compared nodes of the
     first file data and the second file data
    :param formatter: one of three supported formatters - 'stylish', 'plain' or
     'json'. Any other formatter would raise ValueError
    :return: result of formatting with the chosen formatter in string type
    """
    if formatter == 'stylish':
        return stylish.render_stylish(diff)
    if formatter == 'plain':
        return plain.render_plain(diff)
    if formatter == 'json':
        return json.render_json(diff)
    raise ValueError(f'Unknown formatter: {formatter}')
