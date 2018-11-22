"""Unit tests for yamlchecker."""
from pathlib import Path

import pytest

import yamlchecker


TRUTH_FILE = 'truth.yaml'
FAIL_FILE = 'fail.yml'
FAIL_SECTION_FILE = 'fail_section.yaml'
DIRECTORY = 'test_cases'

TRUTH_YAML = """Description: description.
Requirements:
    - req_id
Steps:
    -
        Description: step 1.
        Expected result: result for step 1.
"""

FAIL_YAML = """Description: |
-
    description.
Requirements:
    - req_id
Steps:
    -
        Description: step 1.
        Expected result: result for step 1.
"""

FAIL_SECTION = """Descruption: |
    description.
Steps:
    -
        Description: step 1.
        Expected result: result for step 1.
"""

SECTION = {
    'Description': 'description'
}


@pytest.fixture(autouse=True)
def setup(tmpdir):
    """Setup for unit tests.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    truth_file = tmpdir.join(TRUTH_FILE)
    truth_file.write(TRUTH_YAML)
    fail_file = tmpdir.join(FAIL_FILE)
    fail_file.write(FAIL_YAML)
    fail_section_file = tmpdir.join(FAIL_SECTION_FILE)
    fail_section_file.write(FAIL_SECTION)
    subdir = tmpdir.mkdir(DIRECTORY)
    subdir.join('file1.yaml').write(TRUTH_YAML)
    subdir.join('file2.yml').write(FAIL_YAML)
    subdir.join('file3.txt').write(FAIL_YAML)


def test_truth_file(tmpdir):
    """Test for truth file.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    file = str(tmpdir.join(TRUTH_FILE))
    assert yamlchecker.yaml_checker(Path(file)) == 0


def test_fail_file(tmpdir):
    """Test for fail file.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    file = str(tmpdir.join(FAIL_FILE))
    assert yamlchecker.yaml_checker(Path(file)) == 2


def test_file_with_fail_sections(tmpdir):
    """Test for file with fail sections.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    file = str(tmpdir.join(FAIL_SECTION_FILE))
    assert yamlchecker.yaml_checker(Path(file)) == 2


def test_directory_with_tests(tmpdir):
    """Test for directory with test cases.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    directory = str(tmpdir.join(DIRECTORY))
    assert yamlchecker.yaml_checker(Path(directory)) == 2


def test_truth_section(tmpdir):
    """Test for truth section.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    assert yamlchecker.yamlchecker.check_section(SECTION, 'Description', tmpdir) == 0


def test_fail_section(tmpdir):
    """Test for fail section.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    assert yamlchecker.yamlchecker.check_section(SECTION, 'Steps', tmpdir) == 1
