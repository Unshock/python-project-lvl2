import os
from gendiff import tree
from gendiff.formatter import formatting
from gendiff.parse import parse


def generate_diff(file_path_1: str, file_path_2: str, formatter='stylish'):
    """
    :param file_path_1: path to the first file to compare
    :param file_path_2: path to the second file to compare
    :param formatter: one of three supported formatters ('stylish', 'plain' or
        'json'). 'Stylish' formatter is set by default.
    :return: difference between two files in set format view
    """
    file_1 = get_data(file_path_1)
    file_2 = get_data(file_path_2)
    diff = tree.build(file_1, file_2)
    styled_diff = formatting(diff, formatter)
    return styled_diff


def get_format(file_path: str) -> str:
    """
    :param file_path: path to the file
    :return: file format according to file extension
    """
    _, extension = os.path.splitext(file_path)
    return extension.lower()[1:]


def get_data(file_path: str):
    """
    :param file_path: path to the file
    :return: data of the file in python-ready format
    """
    return parse(open(file_path), get_format(file_path))
