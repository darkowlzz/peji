"""
Generate site data files tests.
"""

import shutil
import json
import os
import peji


def test_generate_site_data_files():
    """Test generates site data files and reads the content to verify the
    integrity of the files.
    """
    peji.generate_site_data_files('tests/test_config.json')
    with open('tests/test_config.json', 'r') as master_config_file:
        # Read master config data and compare the generated files with the
        # master config.
        master_data = json.load(master_config_file)

        with open('public/config.json', 'r') as site_config:
            site_config_data = json.load(site_config)
            assert master_data['title'] == site_config_data['title']
            assert master_data['title-lead'] == site_config_data['title-lead']
            assert master_data['info'] == site_config_data['info']

            for index, cat in enumerate(site_config_data['catalog']):
                with open(os.path.join('public', cat['dataURL']), 'r') as cat_data_file:
                    cat_data = json.load(cat_data_file)
                    assert master_data['catalog'][index] == cat_data

    # Cleanup - deleted the generated content.
    shutil.rmtree('public/')