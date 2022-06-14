import json


def render_json(diff: dict) -> str:
    """
    :param diff: standard diff between two files in dict type
    :return: diff between two files in 'json' format in json-valid string type
    """
    return json.dumps(diff, indent=2)
