"""
buttons provides functions to interact with paypal buttons manager API.
"""

import urllib.parse as ul
import datetime
import os
import requests
from bs4 import BeautifulSoup

API_ENDPOINT = "https://api-3t.paypal.com/nvp"

# Use sandbox API endpoint if PP_SANDBOX env var is found.
if 'PP_SANDBOX' in os.environ:
    API_ENDPOINT = "https://api-3t.sandbox.paypal.com/nvp"


def prepare_post_data(postattr):
    """Takes a request data and appens it with API credentials."""
    post_data = {
        "USER": os.environ['PP_USER'],
        "PWD": os.environ['PP_PWD'],
        "SIGNATURE": os.environ['PP_SIGNATURE'],
        "VERSION": "51.0"
    }
    post_data.update(postattr)
    return post_data


def check_request_failure(resp_text):
    """Checks if the response text contains failure message and returns False
    if the a failure message is found, else returns True.
    """

    if 'ACK=Failure' in resp_text:
        return False
    return True


def create_button(name, price, shipping, ino):
    """Creates a paypal button and returns the button form as string."""
    postattr = {
        "VERSION": "51.0",
        "METHOD": "BMCreateButton",
        "BUTTONCODE": "HOSTED",
        "BUTTONTYPE": "BUYNOW",
        "BUTTONSUBTYPE": "PRODUCTS",
        "BUTTONCOUNTRY": "US",
        "L_BUTTONVAR1": f"item_name={name}",
        "L_BUTTONVAR2": f"amount={str(price)}",
        "L_BUTTONVAR3": f"shipping={str(shipping)}",
        "L_BUTTONVAR4": f"item_number={str(ino)}"
    }
    postdata = prepare_post_data(postattr)
    resp = requests.post(API_ENDPOINT, data=postdata)
    if resp.ok and check_request_failure(resp.text):
        decoded_resp = ul.unquote_plus(resp.text)
        soup = BeautifulSoup(decoded_resp, 'html.parser')
        form = str(soup.form)
        final_button = form.replace('\n', '')
        return final_button

    raise Exception("failed to create button", ul.unquote_plus(resp.text))


def delete_button(button_id):
    """Deletes a paypal button given the button ID."""
    postattr = {
        "METHOD": "BMManageButtonStatus",
        "HOSTEDBUTTONID": button_id,
        "BUTTONSTATUS": "DELETE"
    }
    postdata = prepare_post_data(postattr)
    resp = requests.post(API_ENDPOINT, data=postdata)
    if resp.ok and check_request_failure(resp.text):
        pass
    else:
        raise Exception("failed to delete button", ul.unquote_plus(resp.text))


def get_button_id_from_form(form):
    """Extracts paypal button ID from a given form string."""
    soup = BeautifulSoup(form, 'html.parser')
    btn_id_input = soup.form.find_all("input")[1]
    return btn_id_input.attrs['value']


def get_all_buttons(days):
    """Returns a list of all the buttons created in the last 24 hours."""
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(days=days)
    postattr = {
        "METHOD": "BMButtonSearch",
        "STARTDATE": f"{start_time.isoformat()}Z",
        "ENDDATE": f"{end_time.isoformat()}Z"
    }
    postdata = prepare_post_data(postattr)
    resp = requests.post(API_ENDPOINT, data=postdata)
    if resp.ok and check_request_failure(resp.text):
        res = ul.unquote_plus(resp.text)
        btn_ids = []
        for item in res.split("&"):
            if 'HOSTEDBUTTONID' in item:
                btn_ids.append(item.split("=")[1])
        return btn_ids

    raise Exception("failed to get buttons", ul.unquote_plus(resp.text))
