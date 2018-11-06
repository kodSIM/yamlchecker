"""Unit tests for yamlchecker."""
from pathlib import Path

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


def create_truth_file(tmpdir):
    file = tmpdir.join('file.yaml')
    file.write(TRUTH_YAML)
    return file


def create_fail_file(tmpdir):
    file = tmpdir.join('file.yaml')
    file.write(FAIL_YAML)
    return file


def create_file_with_fail_sections(tmpdir):
    file = tmpdir.join('file.yaml')
    file.write(FAIL_SECTION)
    return file


def test_truth_file(tmpdir):
    file = create_truth_file(tmpdir)
    assert yamlchecker.yaml_checker(Path(str(file))) == 0


def test_fail_file(tmpdir):
    file = create_fail_file(tmpdir)
    assert yamlchecker.yaml_checker(Path(str(file))) == 2


def test_file_with_fail_sections(tmpdir):
    file = create_file_with_fail_sections(tmpdir)
    assert yamlchecker.yaml_checker(Path(str(file))) == 2


def test_truth_section(tmpdir):
    assert yamlchecker.yamlchecker.check_section(SECTION, 'Description', tmpdir) == 0


def test_fail_section(tmpdir):
    assert yamlchecker.yamlchecker.check_section(SECTION, 'Steps', tmpdir) == 1
