import json


def build_diff(data_1, data_2):
    diff = []
    keys = data_1.keys() | data_2.keys()
    for key in sorted(keys):
        if key not in data_1:
            diff.append({
                "key": key,
                "type": "added",
                "value": data_2[key]
            })
        elif key not in data_2:
            diff.append({
                "key": key,
                "type": "deleted",
                "value": data_1[key]
            })
        elif isinstance(data_1[key], dict) and isinstance(data_2[key], dict):
            diff.append({
                "key": key,
                "type": "nested",
                "children": build_diff(data_1[key], data_2[key])
            })
        elif data_1[key] != data_2[key]:
            diff.append({
                "key": key,
                "type": "changed",
                "value1": data_1[key],
                "value2": data_2[key]
            })
        else:
            diff.append({
                "key": key,
                "type": "unchanged",
                "value": data_1[key]
            })
    return diff


def build(data_1, data_2):
    result = {
        "type": "root",
        "children": build_diff(data_1, data_2)
    }
    return json.dumps(result, indent=4)
