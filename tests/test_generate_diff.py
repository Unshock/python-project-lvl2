import pytest

from gendiff.scripts.gendiff import generate_diff
from gendiff.generate_difference import get_data
from gendiff.formatters.stylish import render_stylish
from gendiff.tree import build


def test_generate_diff_1(make_json_file_path_1,
                         make_json_file_path_2, make_result_file_path_1):
    result = generate_diff(make_json_file_path_1, make_json_file_path_2)
    expected_result = make_result_file_path_1
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_2(make_json_file_path_1, make_result_file_path_2):
    result = generate_diff(make_json_file_path_1, make_json_file_path_1)
    expected_result = make_result_file_path_2
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_3(make_yaml_file_path_1,
                         make_yaml_file_path_2, make_result_file_path_1):
    result = generate_diff(make_yaml_file_path_1, make_yaml_file_path_2)
    expected_result = make_result_file_path_1
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_4(make_yaml_file_path_1, make_result_file_path_2):
    result = generate_diff(make_yaml_file_path_1, make_yaml_file_path_1)
    expected_result = make_result_file_path_2
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_5(make_json_file_path_3,
                         make_json_file_path_4, make_result_file_path_3):
    result = generate_diff(make_json_file_path_3, make_json_file_path_4)
    expected_result = make_result_file_path_3
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_6(make_json_file_path_3, make_result_file_path_4):
    result = generate_diff(make_json_file_path_3, make_json_file_path_3)
    expected_result = make_result_file_path_4
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_7(make_yaml_file_path_3,
                         make_yaml_file_path_4, make_result_file_path_3):
    result = generate_diff(make_yaml_file_path_3, make_yaml_file_path_4)
    expected_result = make_result_file_path_3
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_8(make_yaml_file_path_3, make_result_file_path_4):
    result = generate_diff(make_yaml_file_path_3, make_yaml_file_path_3)
    expected_result = make_result_file_path_4
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_9(make_yaml_file_path_3,
                         make_json_file_path_4, make_result_file_path_5):
    result = generate_diff(make_yaml_file_path_3, make_json_file_path_4,
                           formatter='plain')
    expected_result = make_result_file_path_5
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_10(make_yaml_file_path_3,
                          make_json_file_path_4, make_result_file_path_7):
    result = generate_diff(make_yaml_file_path_3, make_json_file_path_4,
                           formatter='json')
    expected_result = make_result_file_path_7
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_11(make_yaml_file_path_4,
                          make_result_file_path_6):
    result = generate_diff(make_yaml_file_path_4, make_yaml_file_path_4,
                           formatter='json')
    expected_result = make_result_file_path_6
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_12(make_json_file_path_3,
                          make_json_file_path_4,
                          make_result_file_path_8):
    file_1 = get_data(make_json_file_path_3)
    file_2 = get_data(make_json_file_path_4)
    result = build(file_1, file_2)
    expected_result = make_result_file_path_8
    with open(expected_result, 'r') as diff:
        assert result == eval(diff.read())


def test_generate_diff_13(make_json_file_path_3,
                          make_json_file_path_4,
                          make_result_file_path_3):
    file_1 = get_data(make_json_file_path_3)
    file_2 = get_data(make_json_file_path_4)
    result = render_stylish(build(file_1, file_2))
    expected_result = make_result_file_path_3
    with open(expected_result, 'r') as diff:
        assert result == diff.read()


def test_generate_diff_14(make_yaml_file_path_4):
    with pytest.raises(ValueError) as wrong_formatter:
        generate_diff(make_yaml_file_path_4, make_yaml_file_path_4,
                      formatter='jsons')
    assert str(wrong_formatter.value) == 'Unknown formatter: jsons'


def test_generate_diff_15(make_result_file_path_1):
    with pytest.raises(ValueError) as wrong_extension:
        generate_diff(make_result_file_path_1, make_result_file_path_1)
    assert str(wrong_extension.value) == 'File format is not supported: txt'
