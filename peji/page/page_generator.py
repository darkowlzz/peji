from bs4 import BeautifulSoup
from peji.page.home import HomeGenerator
from peji.page.shop import ShopGenerator
from peji.page.calendar import CalendarGenerator
from . import SiteType, SITE_TYPE
import sys


def generate_page(data):
    """Generates all the site files."""

    try:
        siteType = SiteType[data[SITE_TYPE]]
    except KeyError as error:
        sys.exit('Unknown site type %r' % error.args)

    if siteType == SiteType.HOME:
        print("Generating Home site...")
        site_generator = HomeGenerator()
    elif siteType == SiteType.SHOP:
        print("Generating Shop site...")
        site_generator = ShopGenerator()
    elif siteType == SiteType.CALENDAR:
        print("Generating Calendar site...")
        site_generator = CalendarGenerator()
    else:
        print("Unknown site type")
        return

    site_generator.generate_html(data)
    site_generator.generate_css(data)
    site_generator.generate_js(data)
