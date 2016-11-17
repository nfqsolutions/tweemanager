#!/usr/bin/env python
import re
from setuptools import setup

def get_version():
    with open('nfq/tweemanager/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')

def readme():
    """
    Returns README.md contents as str
    """
    with open('README.md') as f:
        return f.read()

setup(
    name='tweemanager',
    description='Twitter repository manager monitor and processor',
    long_description=readme(),
    version=get_version(),
    author="NFQ Solutions",
    author_email="solutions@nfq.es",
    packages=[
        'nfq.tweemanager',
        'nfq.tweemanager.getoldtweets',
        ],
    zip_safe=False,
    setup_requires=[
    'pymongo',
    'datetime',
    'docopt',
    'pyquery',
    'simplejson',
    'chardet',
    'tweepy',
    'elasticsearch',
    'mongoengine'],
    entry_points={'console_scripts': ['tweemanager=nfq.tweemanager.tweemanager:tweemanager']}
    )
