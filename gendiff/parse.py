import yaml
import json


def parse(data, format_name):
    """
    :param data: data of file. (file should be opened to be parsed by function)
    :param format_name: one of two supported file formats: 'yaml' or 'json'.
        Any other file format will raise ValueError.
    :return: data in python-ready format
    """
    if format_name == 'yaml' or format_name == 'yml':
        return yaml.load(data, Loader=yaml.CLoader)
    if format_name == 'json':
        return json.load(data)
    raise ValueError(f'File format is not supported: {format_name}')
