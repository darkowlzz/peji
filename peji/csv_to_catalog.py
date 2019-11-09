"""
csv_to_catalog is used to parse, validate and import item data from a CSV file
into a json peji catalog.
"""

import os
import csv
import json
import sys
import requests
from datetime import date
from peji import buttons


PUBLISH_DATE_ENV_VAR = 'PUBLISH_DATE'
IMAGE_URL_PREFIX_ENV_VAR = 'IMAGE_URL_PREFIX'
IMAGE_URL_PREFIX = 'non/existent/image/url/prefix'


def get_data(csvfile):
    """Get data converts the data in a CSV file into the data format of items in
    a catalog. Used with v0.0.3 CSV files.
    """
    image_url_prefix = IMAGE_URL_PREFIX

    # Get image url prefix from env var.
    if IMAGE_URL_PREFIX_ENV_VAR in os.environ:
        image_url_prefix = os.environ[IMAGE_URL_PREFIX_ENV_VAR]

    today = date.today()

    with open(csvfile) as f:
        reader = csv.reader(f)
        next(reader, None)
        items = []
        for row in reader:
            item = {
                'id': row[4],
                'image': f"{image_url_prefix}/{row[4]}.jpeg",
                'title': row[0],
                'description': f"{row[3]} - {row[1]} inches",
                'publishDate': today.strftime('%d %B, %Y'),
                'available': True,
                'price': row[2],
                'button': '',
            }
            item = validate_and_sanitize(item)
            items.append(item)

        return items


def get_data_from_csv(csvfile):
    """Get data from CSV converts the data in a CSV file into the data format of
    items in a catalog. Used with post v0.0.3 CSV files.
    """
    image_url_prefix = IMAGE_URL_PREFIX

    # Get image url prefix from env var.
    if IMAGE_URL_PREFIX_ENV_VAR in os.environ:
        image_url_prefix = os.environ[IMAGE_URL_PREFIX_ENV_VAR]

    custom_date = False
    today = date.today()

    # Check if a custom date is specified in env vars.
    if PUBLISH_DATE_ENV_VAR in os.environ:
        custom_date = True
        today = os.environ[PUBLISH_DATE_ENV_VAR]

    with open(csvfile) as f:
        reader = csv.reader(f)
        next(reader, None)
        items = []
        for row in reader:
            item = {
                'id': row[4],
                'image': f"{image_url_prefix}/{row[4]}.jpeg",
                'title': row[0],
                'description': f"{row[3]} - {row[1]} inches",
                # 'publishDate': today.strftime('%d %B, %Y'),
                'available': bool(int(row[6])),
                'price': row[2],
                'button': '',
                'catalog': row[5],
            }
            # Set the date. This is needed in tests.
            if custom_date:
                item['publishDate'] = today
            else:
                item['publishDate'] = today.strftime('%d %B, %Y')

            item = validate_and_sanitize(item)
            items.append(item)

        return items


def validate_and_sanitize(item):
    # Ensure the price is a number.
    try:
        # TODO: Add float support and ensure paypal accepts decimal values.
        price = int(float(item['price']))
    except ValueError as error:
        sys.exit('data validation failed for ID %s: %r' % (item['id'], error))

    item['price'] = price
    return item


def update_data(data, csvfile, catalog_id):
    """Used in v0.0.3 for updating an existing config file with a CSV data file,
    given a catalog ID. This updated data of only one catalog because the CSV
    file didn't had the catalog ID info.
    """
    targetCatalog = None

    # Get the target catalog.
    for cat in data['catalog']:
        if cat['id'] == catalog_id:
            targetCatalog = cat
            break

    if targetCatalog == None:
        sys.exit('catalog id %s not found' % catalog_id)

    updated_data = get_data(csvfile)

    # Go through the items and update or add items.
    for item in updated_data:
        # Get the item with same ID.
        existing_items = [
            i for i in targetCatalog['items'] if i['id'] == item['id']
        ]
        if len(existing_items) > 1:
            sys.exit('found more than one item with same id %s' %
                     item['id'])
        if len(existing_items) > 0:
            # update the data, existing item.
            existing_item = existing_items[0]
            existing_item['title'] = item['title']
            existing_item['description'] = item['description']
            existing_item['price'] = item['price']
        else:
            # add the item, new addition to items.
            targetCatalog['items'].append(item)

    # Return the updated data.
    return data


def update_release_data(repo_name, csvfile):
    """Pulls previous release data from the given repo, updates that with the
    latest version of the CSV data and generates paypal buttons for any new
    entries. The final json data file can be later posted to the latest release.
    """

    release_url = f"https://api.github.com/repos/{repo_name}/releases"
    r = requests.get(release_url)
    rel_data = r.json()

    data = update_release_data_with_csv(rel_data, csvfile)

    return data


def update_release_data_with_csv(rel_data, csvfile):
    """This processes the release info and updates the latest released data with
    the CSV file and returns the new updated data.
    """
    # Final updated data.
    data = []

    # Data from the CSV file.
    updated_data = get_data_from_csv(csvfile)

    download_url_key = 'browser_download_url'

    # Analyze the release data and update the existing data if available.
    if len(rel_data) == 0:
        # No previous releases. Use the CSV to create first data file.
        print("no previous release found, generating data from CSV only")
    elif len(rel_data) == 1:
        # Check if there's any data file in the assets of the release. If not,
        # create a data file using the CSV. If there's a data file, download the
        # data file and use it along with the CSV to create a new data file.
        print("found a release")
        assets = rel_data[0]['assets']
        if len(assets) > 0:
            print("found a data file asset in the release, using this as existing data")
            # Asset exists. Download the data file and assign it to the data
            # var.
            dataURL = assets[0][download_url_key]
            r = requests.get(dataURL)
            data = r.json()
        else:
            print("no assets found, generating data from CSV only")
    else:
        # There are more than one releases. Check if the latest release has any
        # data file in assets. If not, use the data file asset from the previous
        # releases along with the CSV file to create a new data file.
        print("found multiple releases")

        # Checking assets of the releases one by one until data file asset is
        # found.
        dataURL = ""
        for rel in rel_data:
            assets = rel['assets']
            if len(assets) > 0:
                print(
                    "found a data file asset in release %r, using this as existing data" % rel['name'])
                dataURL = assets[0][download_url_key]
                break
            else:
                print(
                    "found no data file asset in release %r, checking the previous release" % rel['name'])

        if dataURL:
            r = requests.get(dataURL)
            data = r.json()
        else:
            print("no assets found, generating data from CSV only")

    data = get_catalog_data(data, updated_data)
    return data


def get_catalog_data(cat_data, data):
    """Given an existing catalog data and a list of new data, convert the list
    into catalog data format with items separated based on their catalog ID and
    update any existing items with the CSV data.
    """
    # Parse through each of the items and add them into their own catalog.
    for item in data:
        cat_id = item["catalog"]

        # Remove the catalog info from the item because it'll be placed under
        # a catalog.
        del item["catalog"]

        # Check if there's an existing catalog of the ID found in the item. If
        # not, create the catalog entry and then add the item under that
        # catalog.
        existing_catalog = [
            i for i in cat_data if i["id"] == cat_id
        ]

        if len(existing_catalog) > 1:
            sys.exit('found more than one catalog with same id %s' % cat_id)
        if len(existing_catalog) > 0:
            # Found existing catalog, append the item in the catalog.
            catalog = existing_catalog[0]

            existing_items = [
                i for i in catalog['items'] if i['id'] == item['id']
            ]
            if len(existing_items) > 1:
                sys.exit('found more than one item with same id %s' %
                         item['id'])
            if len(existing_items) > 0:
                # update the data, existing item.
                existing_item = existing_items[0]
                existing_item['title'] = item['title']
                existing_item['description'] = item['description']
                existing_item['price'] = item['price']
                existing_item['available'] = item['available']
                existing_item['publishDate'] = item['publishDate']
            else:
                catalog['items'].append(item)
        else:
            # No existing catalog. Create a new catalog and append the item in
            # the catalog.
            cat = {
                "id": cat_id,
                "category": "",
                "items": [],
            }
            cat['items'].append(item)
            cat_data.append(cat)

    return cat_data
