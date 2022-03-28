import pytest
from gendiff.scripts.gendiff import generate_diff
import json


@pytest.fixture
def make_json_1():
    result = json.load(open('gendiff/files/file1.json'))
    return result


@pytest.fixture
def make_json_2():
    result = json.load(open('gendiff/files/file2.json'))
    return result


def test_generate_diff(make_json_1, make_json_2):
    result = generate_diff(make_json_1, make_json_2)
    assert result == {
    "- follow": false,
    "host": "hexlet.io",
    "- proxy": 123.234.53.22,
    "- timeout": 50,
    "+ timeout": 20,
    "+ verbose": true,
    }