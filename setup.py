"""
Installation for peji.
"""

from setuptools import setup, find_packages

setup(
    name='peji',
    version='0.1.0',
    # py_modules=['peji', 'peji.buttons', 'peji.page'],
    packages=find_packages(),
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
