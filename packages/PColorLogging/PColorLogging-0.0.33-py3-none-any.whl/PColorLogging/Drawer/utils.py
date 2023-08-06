import json


def _read_json_file(json_file_path):
    return json.loads(open(json_file_path, 'r').read())
