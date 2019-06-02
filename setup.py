"""
Installation for peji.
"""

from setuptools import setup

setup(
    name='peji',
    version='0.1.0',
    py_modules=['peji', 'buttons', 'page'],
    install_requires=[
        'Click',
        'bs4',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        peji=peji:cli
    ''',
)
