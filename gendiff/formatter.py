from gendiff.formatters import plain, stylish, json


def formatting(formatter: str):
    if formatter == 'stylish':
        return stylish.render_stylish
    elif formatter == 'plain':
        return plain.render_plain
    elif formatter == 'json':
        return json.render_json
    raise ValueError(f'Unknown formatter: {formatter}')
