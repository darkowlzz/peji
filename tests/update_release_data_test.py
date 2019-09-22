"""
Update release data tests.
"""

import os
import json
from peji import csv_to_catalog
import pytest


TEST_CSV_FILE_NO_RELEASE = 'tests/testdata/data-post0.0.3-no-release.csv'
EXPECTED_DATA_FILE_NO_RELEASE = 'tests/testdata/data-post0.0.3-no-release.json'
TEST_CSV_FILE_WITH_RELEASE = 'tests/testdata/data-post0.0.3-with-release.csv'
EXPECTED_DATA_FILE_WITH_RELEASE = 'tests/testdata/data-post0.0.3-with-release.json'


def test_get_catalog_data_no_release():
    """Test generating data file with no existing data file from previous
    release.
    """
    os.environ[csv_to_catalog.PUBLISH_DATE_ENV_VAR] = "22 September, 2019"
    os.environ[csv_to_catalog.IMAGE_URL_PREFIX_ENV_VAR] = 'https://test/static'
    # Read CSV data.
    csv_data = csv_to_catalog.get_data_from_csv(TEST_CSV_FILE_NO_RELEASE)
    # Data from previous release.
    existing_data = []

    got_data = csv_to_catalog.get_catalog_data(existing_data, csv_data)

    with open(EXPECTED_DATA_FILE_NO_RELEASE) as expected_file:
        expected_data = json.load(expected_file)
        assert got_data == expected_data


def test_get_catalog_data_with_release():
    """Test generating data file with existing data file from previous release.
    """
    os.environ[csv_to_catalog.PUBLISH_DATE_ENV_VAR] = "22 September, 2019"
    os.environ[csv_to_catalog.IMAGE_URL_PREFIX_ENV_VAR] = 'https://test/static'
    # Read CSV data.
    csv_data = csv_to_catalog.get_data_from_csv(TEST_CSV_FILE_WITH_RELEASE)
    # Data from previous release.
    with open(EXPECTED_DATA_FILE_NO_RELEASE) as existing_data_file:
        existing_data = json.load(existing_data_file)

    got_data = csv_to_catalog.get_catalog_data(existing_data, csv_data)

    with open(EXPECTED_DATA_FILE_WITH_RELEASE) as expected_file:
        expected_data = json.load(expected_file)
        assert got_data == expected_data
