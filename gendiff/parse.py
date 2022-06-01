import yaml
import json


def parse(data, format_name):
    if format_name == 'yaml' or format_name == 'yml':
        return yaml.load(data, Loader=yaml.CLoader)
    elif format_name == 'json':
        return json.load(data)
    raise ValueError(f'File format is not supported: {format_name}')
