"""Unit tests for yamlchecker."""
import pytest

import yamlchecker


TRUTH_YAML = """
Description: description.
Requirements: req_id
Steps:
    -
        Description: step 1.
        Expected result: result for step 1.
"""
FAIL_YAML = """
Description: |
-
    description.
Requirements: req_id
Steps:
    -
        Description: step 1.
        Expected result: result for step 1.
"""
FAIL_SECTION = """
Descruption: |
    description.
Steps:
    -
        Description: step 1.
        Expected result: result for step 1.
"""
SECTION = {
    'Description': 'description'
}


def create_truth_file(tmp_path):
    file = tmp_path / 'file.yaml'
    file.write_text(TRUTH_YAML)
    return file


def create_fail_file(tmp_path):
    file = tmp_path / 'file.yaml'
    file.write_text(FAIL_YAML)
    return file


def create_file_with_fail_sections(tmp_path):
    file = tmp_path / 'file.yaml'
    file.write_text(FAIL_SECTION)
    return file


def test_truth_file(tmp_path):
    file = create_truth_file(tmp_path)
    assert yamlchecker.yaml_checker(file) == 0


def test_fail_file(tmp_path):
    file = create_fail_file(tmp_path)
    assert yamlchecker.yaml_checker(file) == 2


def test_file_with_fail_sections(tmp_path):
    file = create_file_with_fail_sections(tmp_path)
    assert yamlchecker.yaml_checker(file) == 2


def test_truth_section(tmp_path):
    assert yamlchecker.yamlchecker.check_section(SECTION, 'Description', tmp_path) == 0


def test_fail_section(tmp_path):
    assert yamlchecker.yamlchecker.check_section(SECTION, 'Steps', tmp_path) == 1
