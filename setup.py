# -*- coding: utf8 -*-
# system imports:
import re

from codecs import open as open
from setuptools import setup
# package imports:
# 3rd party packages imports:


def get_version():
    with open('nfq/tweemanager/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


def readme():
    ''' Returns README.md contents as str '''
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='tweemanager',
    description='Twitter repository manager monitor and processor',
    long_description=readme(),
    version=get_version(),
    author="NFQ Solutions",
    author_email="solutions@nfq.es",
    namespace_packages=['nfq'],
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
    entry_points={'console_scripts': [
        'tweemanager=nfq.tweemanager.tweemanager:tweemanager']},
    classifiers=[
        'Development Status :: Beta-rc',
        'Intended Audience :: Developers, Administrators',
        'Topic :: Text Processing :: General',
        'License :: AGPL',
        'Programming Language :: Python :: 3.5'
    ]
)
