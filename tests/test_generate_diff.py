import pytest
from gendiff.scripts.gendiff import generate_diff


@pytest.fixture
def make_json_file_path_1():
    json_file_path_1 = 'tests/fixtures/file1.json'
    return json_file_path_1


@pytest.fixture
def make_json_file_path_2():
    json_file_path_2 = 'tests/fixtures/file2.json'
    return json_file_path_2


def test_generate_diff(make_json_file_path_1, make_json_file_path_2):
    result = generate_diff(make_json_file_path_1, make_json_file_path_2)
    with open('tests/fixtures/test_result_1.txt', 'r') as diff:
        assert result == diff.read()

def test_generate_diff_2(make_json_file_path_1):
    result = generate_diff(make_json_file_path_1, make_json_file_path_1)
    with open('tests/fixtures/test_result_2.txt', 'r') as diff:
        assert result == diff.read()

