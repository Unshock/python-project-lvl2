import json


def render_json(diff: dict) -> str:
    return json.dumps(diff, indent=2)
