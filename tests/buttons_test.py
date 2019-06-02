"""
Buttons Tests.
"""

from peji import buttons
import peji


def test_make_delete_buttons():
    """Test make buttons and delete all the buttons from config file."""
    peji.delete_all_paypal_buttons_for_days(10)
    peji.make_paypal_buttons('tests/test_config.json')
    btns = buttons.get_all_buttons(1)
    existing_buttons = len(btns)
    assert existing_buttons == 8
    peji.delete_paypal_buttons_from_config('tests/test_config.json')
    btns = buttons.get_all_buttons(1)
    existing_buttons = len(btns)
    assert existing_buttons == 0
