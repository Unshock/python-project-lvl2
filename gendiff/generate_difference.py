from . import generator


def generate_diff(file_path_1, file_path_2):
    file_1 = generator.load_file_by_path(file_path_1)
    file_2 = generator.load_file_by_path(file_path_2)
    checking_list = generator.make_checking_list(file_1, file_2)
    diff = generator.make_stylish_diff(checking_list)
    return diff
