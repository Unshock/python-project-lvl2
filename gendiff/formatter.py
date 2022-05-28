from gendiff.formatters import plain, stylish


def set_format(formatter):
    formats = {
        'stylish': stylish.make_stylish_diff,
        'plain': plain.make_plain_diff
    }
    if formatter not in formats.keys():
        raise Exception('There is no such formatter')
    else:
        return formats[formatter]
