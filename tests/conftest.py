import pytest
import os


FIXTURES_FOLDER = 'fixtures'


@pytest.fixture
def make_json_file_path_1():
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER, 'file1.json')
    return json_file_path


@pytest.fixture
def make_json_file_path_2():
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER, 'file2.json')
    return json_file_path


@pytest.fixture
def make_json_file_path_3():
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER, 'file3.json')
    return json_file_path


@pytest.fixture
def make_json_file_path_4():
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER, 'file4.json')
    return json_file_path


@pytest.fixture
def make_yaml_file_path_1():
    yaml_file_path = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER, 'file1.yaml')
    return yaml_file_path


@pytest.fixture
def make_yaml_file_path_2():
    yaml_file_path = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER, 'file2.yaml')
    return yaml_file_path


@pytest.fixture
def make_yaml_file_path_3():
    yaml_file_path = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER, 'file3.yaml')
    return yaml_file_path


@pytest.fixture
def make_yaml_file_path_4():
    yaml_file_path = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER, 'file4.yaml')
    return yaml_file_path


@pytest.fixture
def make_result_file_path_1():
    result_file_path = os.path.join(os.path.dirname(__file__),
                                    FIXTURES_FOLDER, 'test_result_1.txt')
    return result_file_path


@pytest.fixture
def make_result_file_path_2():
    result_file_path = os.path.join(os.path.dirname(__file__),
                                    FIXTURES_FOLDER, 'test_result_2.txt')
    return result_file_path


@pytest.fixture
def make_result_file_path_3():
    result_file_path = os.path.join(os.path.dirname(__file__),
                                    FIXTURES_FOLDER, 'test_result_3.txt')
    return result_file_path


@pytest.fixture
def make_result_file_path_4():
    result_file_path = os.path.join(os.path.dirname(__file__),
                                    FIXTURES_FOLDER, 'test_result_4.txt')
    return result_file_path


@pytest.fixture
def make_result_file_path_5():
    result_file_path = os.path.join(os.path.dirname(__file__),
                                    FIXTURES_FOLDER, 'test_result_5.txt')
    return result_file_path


@pytest.fixture
def make_result_file_path_6():
    result_file_path = os.path.join(os.path.dirname(__file__),
                                    FIXTURES_FOLDER, 'test_result_6.txt')
    return result_file_path
