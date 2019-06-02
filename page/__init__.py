"""
Site page generator.
"""

import abc
from enum import Enum


class SiteType(Enum):
    """SiteType defines different types of sites."""
    HOME = 1
    SHOP = 2


# Site type attribute name in peji config.
SITE_TYPE = "siteType"


class PageGenerator(metaclass=abc.ABCMeta):
    """Abstract class for a page generator. This class must be extended to add new page
    generators."""
    @abc.abstractmethod
    def generate_html(self, data):
        """Method to generate html files."""
        raise NotImplementedError(
            'users must define generate_html to use this base class')

    @abc.abstractmethod
    def generate_css(self, data):
        """Method to generate css files."""
        raise NotImplementedError(
            'users must define generate_css to use this base class')

    @abc.abstractmethod
    def generate_js(self, data):
        """Method to generate js files."""
        raise NotImplementedError(
            'users must define generate_js to use this base class')
