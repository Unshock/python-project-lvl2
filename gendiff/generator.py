def normalize_value(value):
    python_to_js = {
        False: "alse",
        True: "true",
        None: "null",
    }
    if isinstance(value, dict):
        return value
    else:
        return python_to_js[value] if\
            isinstance(value, bool) or value is None else value


def make_checking_list_elem(key, *args, status="undefined"):
    if status == "undefined":
        status = get_status(args[0], args[1])

    if len(args) == 2 and status != "unchanged":
        value = (args[0], args[1])
    else:
        value = args[0]

    if status == "updated, needs DFS":
        value = make_checking_list(args[0], args[1])

    elem = {"name": key,
            "status": status,
            "value": value,
            }
    return elem


def get_status(value1, value2):
    if isinstance(value1, dict) and isinstance(value2, dict):
        return "updated, needs DFS"
    if value1 == value2:
        return "unchanged"
    return "updated"


def make_checking_list(data_1, data_2):
    diff = []
    for key, value in data_1.items():
        value_file_1 = normalize_value(value)
        if key in data_2.keys():
            value_file_2 = normalize_value(data_2[key])
            diff.append(
                make_checking_list_elem(key, value_file_1, value_file_2))
        else:
            diff.append(
                make_checking_list_elem(key, value_file_1, status="deleted"))

    for key in (data_2.keys() - data_1.keys()):
        value_file_2 = normalize_value(data_2[key])
        diff.append(make_checking_list_elem(key, value_file_2, status="added"))

    diff.sort(key=lambda node: node["name"])
    return diff


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
                "value1": data_1[key]
            })
    return diff


def build(data_1, data_2):
    return {
        "type": "root",
        "children": build_diff(data_1, data_2)
    }
