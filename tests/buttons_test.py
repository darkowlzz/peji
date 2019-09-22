"""
Buttons Tests.
"""

from peji import buttons
import peji

TEST_CONFIG_FILE = 'tests/testdata/test_config-post0.0.3.json'


def test_make_delete_buttons():
    """Test make buttons and delete all the buttons from config file."""
    peji.delete_all_paypal_buttons_for_days(100)
    peji.make_paypal_buttons(TEST_CONFIG_FILE)
    btns = buttons.get_all_buttons(100)
    existing_buttons = len(btns)
    assert existing_buttons == 9
    peji.delete_paypal_buttons_from_config(TEST_CONFIG_FILE)
    btns = buttons.get_all_buttons(100)
    existing_buttons = len(btns)
    assert existing_buttons == 0
