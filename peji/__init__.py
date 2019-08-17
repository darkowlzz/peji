"""
peji command line interface
"""

import json
import sys
import os
import importlib.resources as pkg_resources
import click
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from peji import buttons
from peji import csv_to_catalog
from peji.page import page_generator, schemas


def next_item(data):
    """Takes a data dictionary and yields the items under each catalog. It is
    generator function.
    """

    try:
        for cat in data['catalog']:
            for item in cat['items']:
                yield item
    except KeyError as error:
        sys.exit('%r not found in the config' % error.args)
    except TypeError as error:
        sys.exit('unexpected data type: %r' % error.args)


def write_to_file(data, file_desc):
    """Takes a dict and writes json serialized data to the file descriptor."""
    click.echo('updating config file...')
    file_desc.seek(0)
    file_desc.truncate(0)
    json.dump(data, file_desc, indent=2)


def make_paypal_buttons(configfile):
    """Takes a config json file, parses it for catalog items and creates paypal
    buttons for the items.
    """
    with open(configfile, 'r+') as json_file:
        data = json.load(json_file)
        for item in next_item(data):
            if not item['button'] and item['available']:
                click.echo('creating button for %r' % item['title'])
                form = buttons.create_button(
                    item['title'], item['price'], 5, item['id'])
                item['button'] = form

        write_to_file(data, json_file)


def delete_paypal_buttons_from_config(configfile):
    """Takes a config json file, parses it for catalog items and deletes the
    associated paypal buttons for the items.
    """
    with open(configfile, 'r+') as json_file:
        data = json.load(json_file)
        for item in next_item(data):
            if item['button']:
                click.echo('deleting button for %r' % item['title'])
                button_id = buttons.get_button_id_from_form(item['button'])
                buttons.delete_button(button_id)
                item['button'] = ''

        write_to_file(data, json_file)


def delete_all_paypal_buttons_for_days(days):
    """Deletes all the buttons created in within the given days."""
    btn_ids = buttons.get_all_buttons(int(days))
    for i in btn_ids:
        click.echo('deleting button ID %r' % i)
        buttons.delete_button(i)


def get_all_paypal_buttons(days):
    """Prints the IDs of all the buttons created in the given days."""
    btn_ids = buttons.get_all_buttons(int(days))
    for i in btn_ids:
        print(i)


def truncate_all_buttons(configfile):
    """Truncates buttons of all the items in the given config file."""
    with open(configfile, 'r+') as json_file:
        data = json.load(json_file)
        for item in next_item(data):
            if item['button']:
                click.echo('truncating button for %r' % item['title'])
                item['button'] = ''

        write_to_file(data, json_file)


def update_catalog_data(configfile, csvfile, catalog_id):
    with open(configfile, 'r+') as json_file:
        data = json.load(json_file)
        data = csv_to_catalog.update_data(data, csvfile, catalog_id)
        write_to_file(data, json_file)


def generate_site_data_files(configfile):
    """Reads the master config file, creates a site config file and data files"""
    with open(configfile, 'r') as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError as error:
            sys.exit('failed to load json: %r' % error)

        # Validate the data.
        try:
            validate_site_data(data)
        except ValidationError as error:
            sys.exit('data schema validation failed: %r' % error)

        # Ensure that public/data dir exists.
        site_data_dir = os.path.join('public', 'data')
        if not os.path.exists(site_data_dir):
            os.makedirs(site_data_dir)
        # Create data files for each catalog entry.
        try:
            for cat in data['catalog']:
                cat_file_path = os.path.join(site_data_dir, cat['id']+'.json')
                click.echo('generating catalog data file %r' % cat_file_path)
                with open(cat_file_path, 'w') as cat_file:
                    json.dump(cat, cat_file, indent=2)
                # Delete category item list from config.
                del cat['items']
                # Add relative links to the data files in the config file. This path
                # should be relative to the public dir.
                cat['dataURL'] = os.path.relpath(cat_file_path, 'public')
        except KeyError as error:
            click.echo('no %r found, generating rest of the files...' %
                       error.args)

        # Write site config.
        site_config_path = os.path.join('public', 'config.json')
        click.echo('generating site config %r' % site_config_path)
        with open(site_config_path, 'w') as config_file:
            json.dump(data, config_file, indent=2)


def validate_site_data(data):
    """Validates site config data using an appropriate schema."""
    try:
        schema = pkg_resources.read_text(
            schemas, schema_for_site_type(data['siteType']))
    except KeyError as error:
        sys.exit('%r not found in the config' % error.args)

    schema_data = json.loads(schema)
    validate(instance=data, schema=schema_data)
    click.echo('data validation successful')


def schema_for_site_type(site_type):
    """Returns file name of schema for a given site type."""
    return {
        "HOME": "home-schema.json",
        "SHOP": "shop-schema.json",
        "CALENDAR": "calendar-schema.json",
    }[site_type]


def generate_site_files(configfile):
    """Reads the configfile and generates site code based on the config"""
    with open(configfile, 'r') as json_file:
        data = json.load(json_file)
        public_dir = 'public'
        # Create public dir if not exists.
        if not os.path.exists(public_dir):
            os.makedirs(public_dir)

        page_generator.generate_page(data)


############ Config Subcommand ###########

@click.group()
def config():
    """Group of commands to process the config file."""


@click.command()
@click.argument('configfile')
def truncate_buttons(configfile):
    """Truncates all the buttons."""
    truncate_all_buttons(configfile)


@click.command()
@click.argument('configfile')
@click.argument('csvfile')
@click.argument('catalog_id')
def update_data(configfile, csvfile, catalog_id):
    """Updates data under a catalog from a CSV file."""
    update_catalog_data(configfile, csvfile, catalog_id)


# Add commands to config subcommand group.
config.add_command(truncate_buttons)
config.add_command(update_data)


############ Page Subcommand ############

@click.group()
def page():
    """Group of commands for generating site page."""


@click.command()
@click.argument('configfile')
def generate_site_data(configfile):
    """Generate all the site data files, including the site config data."""
    generate_site_data_files(configfile)


@click.command()
@click.argument('configfile')
def generate_site(configfile):
    """Generate html, js and css files for the site."""
    generate_site_files(configfile)


# Add commands to page subcommand group.
page.add_command(generate_site_data)
page.add_command(generate_site)


############ Button Subcommand ############

@click.group()
def button():
    """Group of commands related to paypal buttons."""


@click.command()
@click.argument('configfile')
def make_buttons(configfile):
    """Make buttons for all the items in the config file."""
    make_paypal_buttons(configfile)


@click.command()
@click.argument('configfile')
def delete_all_buttons(configfile):
    """Delete buttons from all the items in the config file."""
    delete_paypal_buttons_from_config(configfile)


@click.command()
@click.argument('days')
def get_all_buttons(days):
    """Print IDs of all the buttons created in the given days."""
    get_all_paypal_buttons(days)


@click.command()
@click.argument('days')
def delete_all_buttons_for_days(days):
    """Deletes all the buttons created within the given days."""
    delete_all_paypal_buttons_for_days(days)


# Add commands to button subcommand group.
button.add_command(make_buttons)
button.add_command(delete_all_buttons)
button.add_command(get_all_buttons)
button.add_command(delete_all_buttons_for_days)


############ Cli root commands #############

@click.group()
def cli():
    """Configure and generate peji site."""


# Add commands to cli command group.
cli.add_command(config)
cli.add_command(page)
cli.add_command(button)
