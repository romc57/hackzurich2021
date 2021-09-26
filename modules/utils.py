import json


def load_json_file(path):
    with open(path, 'r') as file:
        return json.loads(file.read())


def write_json_file(path, json_dict):
    with open(path, 'w') as file:
        file.write(json.dumps(json_dict))
