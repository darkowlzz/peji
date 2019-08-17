"""
csv_to_catalog is used to parse, validate and import item data from a CSV file
into a json peji catalog.
"""

import os
import csv
import json
import sys
from datetime import date

IMAGE_URL_PREFIX_ENV_VAR = 'IMAGE_URL_PREFIX'
IMAGE_URL_PREFIX = 'non/existent/image/url/prefix'


def get_data(csvfile):
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
                'image': f"{image_url_prefix}/{row[4]}.JPG",
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
            # update the data
            existing_item = existing_items[0]
            existing_item['title'] = item['title']
            existing_item['description'] = item['description']
            existing_item['price'] = item['price']
        else:
            # add the item
            targetCatalog['items'].append(item)

    # Return the updated data.
    return data
