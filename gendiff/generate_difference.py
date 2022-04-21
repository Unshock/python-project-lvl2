from . import generator
from . import stylish


def generate_diff(file_path_1, file_path_2, format='stylish'):
    formats = {
        'stylish': stylish.make_stylish_diff,
        'wtoroi': stylish.make_stylish_diff
    }
    file_1 = generator.load_file_by_path(file_path_1)
    file_2 = generator.load_file_by_path(file_path_2)
    checking_list = generator.make_checking_list(file_1, file_2)
    diff = formats[format](checking_list)
    return diff
