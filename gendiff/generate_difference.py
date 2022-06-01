import os
from gendiff import tree
from gendiff.formatter import formatting
from gendiff.parse import parse


def generate_diff(file_path_1, file_path_2, formatter='stylish'):
    file_1 = get_data(file_path_1)
    file_2 = get_data(file_path_2)
    diff = tree.build(file_1, file_2)
    styled_diff = formatting(formatter)(diff)
    return styled_diff


def get_format(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension.lower()[1:]


def get_data(file_path: str):
    return parse(open(file_path), get_format(file_path))
