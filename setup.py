#-*- coding: utf-8 -*-

"""
    glassdoor
    ~~~~~~~~~

    Setup
    `````

    $ pip install glassdoor
"""

from distutils.core import setup

setup(
    name='glassdoor',
    version='0.0.2',
    url='http://github.com/hackerlist/glassdoor',
    author='mek',
    author_email='m@hackerlist.net',
    packages=[
        'glassdoor',
        'test'
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
        'requests >= 1.1.0',
        'BeautifulSoup >= 3.2.1',
    ],
    scripts=[
        "scripts/glassdoor"
        ],
    description="Glassdoor Python API",
    long_description=open('README.md').read(),
)
