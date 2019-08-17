"""
Update catalog data tests.
"""

import os
import json
from peji import csv_to_catalog
import pytest


TEST_CONFIG_FILE = 'tests/testdata/test_update_shop.json'
TEST_CSV_FILE = 'tests/testdata/data.csv'


def test_update_data():
    """Test reads an existing catalog config, reads updated data from a CSV
    file and updates the data in the existing catalog.
    """
    with open(TEST_CONFIG_FILE, 'r') as master_config_file:
        existing_data = json.load(master_config_file)

        # Check if it fails when catalog ID is not found.
        with pytest.raises(SystemExit):
            csv_to_catalog.update_data(
                existing_data, TEST_CSV_FILE, 1)

        # Check if existing data is updated and new items are added.
        # Also check if the IMAGE_URL_PREFIX env var is picked.
        os.environ[csv_to_catalog.IMAGE_URL_PREFIX_ENV_VAR] = 'https://test/static'
        updated_data = csv_to_catalog.update_data(
            existing_data, TEST_CSV_FILE, '1')
        items = updated_data['catalog'][0]['items']

        # Update check.
        assert items[0]['title'] == 'Look Deeper 0_0'
        # Item append check.
        assert items[4]['title'] == 'TestArt'
        # IMAGE_URL_PREFIX env var check.
        assert items[4]['image'] == 'https://test/static/5.JPG'
