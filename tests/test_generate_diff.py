import pytest
import json
from gendiff.scripts.gendiff import generate_diff


@pytest.fixture
def make_json_file_path_1():
    json_file_path_1 = 'gendiff/files/file1.json'
    return json_file_path_1


@pytest.fixture
def make_json_file_path_2():
    json_file_path_2 = 'gendiff/files/file2.json'
    return json_file_path_2


def test_generate_diff(make_json_file_path_1, make_json_file_path_2):
    result = generate_diff(make_json_file_path_1, make_json_file_path_2)
    diff = '{\n' \
           '  - follow: false\n' \
           '    host: hexlet.io\n' \
           '  - proxy: 123.234.53.22\n' \
           '  - timeout: 50\n' \
           '  + timeout: 20\n' \
           '  + verbose: true\n' \
           '}'

    #result_diff = json.dumps(diff, indent=2)
    assert result == diff
