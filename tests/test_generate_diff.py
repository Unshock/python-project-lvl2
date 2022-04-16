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

@pytest.fixture
def make_json_file_path_3():
    json_file_path_1 = 'tests/fixtures/file3.json'
    return json_file_path_1


@pytest.fixture
def make_json_file_path_4():
    json_file_path_2 = 'tests/fixtures/file4.json'
    return json_file_path_2

@pytest.fixture
def make_yaml_file_path_1():
    yaml_file_path_1 = 'tests/fixtures/file1.yaml'
    return yaml_file_path_1


@pytest.fixture
def make_yaml_file_path_2():
    yaml_file_path_2 = 'tests/fixtures/file2.yaml'
    return yaml_file_path_2


def test_generate_diff_1(make_json_file_path_1, make_json_file_path_2):
    result = generate_diff(make_json_file_path_1, make_json_file_path_2)
    with open('tests/fixtures/test_result_1.txt', 'r') as diff:
        assert result == diff.read()


def test_generate_diff_2(make_json_file_path_1):
    result = generate_diff(make_json_file_path_1, make_json_file_path_1)
    with open('tests/fixtures/test_result_2.txt', 'r') as diff:
        assert result == diff.read()


def test_generate_diff_3(make_yaml_file_path_1, make_yaml_file_path_2):
    result = generate_diff(make_yaml_file_path_1, make_yaml_file_path_2)
    with open('tests/fixtures/test_result_1.txt', 'r') as diff:
        assert result == diff.read()


def test_generate_diff_4(make_yaml_file_path_1):
    result = generate_diff(make_yaml_file_path_1, make_yaml_file_path_1)
    with open('tests/fixtures/test_result_2.txt', 'r') as diff:
        assert result == diff.read()


def test_generate_diff_5(make_json_file_path_3, make_json_file_path_4):
    result = generate_diff(make_json_file_path_3, make_json_file_path_4)
    with open('tests/fixtures/test_result_3.txt', 'r') as diff:
        assert result == diff.read()


def test_generate_diff_6(make_json_file_path_3):
    result = generate_diff(make_json_file_path_3, make_json_file_path_3)
    with open('tests/fixtures/test_result_4.txt', 'r') as diff:
        assert result == diff.read()

