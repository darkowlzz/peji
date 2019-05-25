"""
peji cli helps interact with peji config file.
"""

import json
import sys
import click
import buttons
import os


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


def make_buttons(configfile):
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


def delete_buttons(configfile):
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


def delete_all(days):
    """Deletes all the buttons created in within the given days."""
    btn_ids = buttons.get_all_buttons(int(days))
    for i in btn_ids:
        click.echo('deleting button ID %r' % i)
        buttons.delete_button(i)


def get_all(days):
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


def update_site_config_data_url(configfile, url):
    """Updates data URL in the site config file."""
    with open(configfile, 'w') as file:
        file.write(f"var dataURL = \"{url}\"")


def generate_site_data_files(configfile):
    """Reads the master config file, creates a site config file and data files"""
    with open(configfile, 'r') as json_file:
        data = json.load(json_file)
        # Ensure that public/data dir exists.
        site_data_dir = os.path.join('public', 'data')
        if not os.path.exists(site_data_dir):
            os.makedirs(site_data_dir)
        # Create data files for each catalog entry.
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

        # Write site config.
        site_config_path = os.path.join('public', 'config.json')
        click.echo('generating site config %r' % site_config_path)
        with open(site_config_path, 'w') as config_file:
            json.dump(data, config_file, indent=2)


@click.group()
def cli():
    """The main Click cli function."""


@click.command()
@click.argument('configfile')
def make(configfile):
    """Make buttons for all the items in the config file."""
    make_buttons(configfile)


@click.command()
@click.argument('configfile')
def delete(configfile):
    """Delete buttons from all the items in the config file."""
    delete_buttons(configfile)


@click.command()
@click.argument('days')
def get_all_buttons(days):
    """Print IDs of all the buttons created in the given days."""
    get_all(days)


@click.command()
@click.argument('days')
def delete_all_for_days(days):
    """Deletes all the buttons created within the given days."""
    delete_all(days)


############ Config Subcommand ###########

@click.group()
def config():
    """Group of commands to process the config file."""


@click.command()
@click.argument('configfile')
def truncate_buttons(configfile):
    """Truncates all the buttons."""
    truncate_all_buttons(configfile)


############ Site Subcommand ############

@click.group()
def site():
    """Group of commands for processing site config."""


@click.command()
@click.argument('configfile', nargs=1)
@click.argument('url', nargs=1)
def update_site_data(configfile, url):
    """Update data url in the given site config."""
    update_site_config_data_url(configfile, url)


@click.command()
@click.argument('configfile')
def generate_site_data(configfile):
    """Generate all the site data files, including the site config data."""
    generate_site_data_files(configfile)


# Add commands to config subcommand group.
config.add_command(truncate_buttons)


# Add commands to site subcommand group.
site.add_command(update_site_data)
site.add_command(generate_site_data)


# Add commands to cli command group.
cli.add_command(make)
cli.add_command(delete)
cli.add_command(get_all_buttons)
cli.add_command(delete_all_for_days)
cli.add_command(config)
cli.add_command(site)
