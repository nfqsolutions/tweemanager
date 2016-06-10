# -*- coding: utf-8 -*-
import sys
import os
import re
import shutil
from setuptools import setup, find_packages


def get_version():
    with open('tweemanager/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


def readme():
    ''' Returns README.md contents as str '''
    with open('README.md') as f:
        return f.read()


data_files = [
    (os.path.expanduser('~/.tweemanager'), ['.tweemanager'])
]

install_requires = [
    'pymongo',
    'docopt',
    'pyquery',
    'simplejson',
    'chardet',
    'tweepy',
    'mongoengine'
]

lint_requires = [
    'pep8',
    'pyflakes'
]

tests_require = []
dependency_links = []
setup_requires = []
extras_require = {
    'test': tests_require,
    'all': install_requires + tests_require,
    'docs': ['sphinx'] + tests_require,
    'lint': lint_requires
}

if 'nosetests' in sys.argv[1:]:
    setup_requires.append('nose')

setup(
    name='tweemanager',
    version=get_version(),
    description='Twitter repository manager monitor and processor.',
    long_description=readme(),
    author='Hugo Marrao',
    author_email='hugo.marrao@nfq.es',
    license='MIT',
    url='https://github.com/ekergy/tweemanager',
    keywords=['json', 'mongo', 'elasticsearch', 'twitter', 'monitor'],
    packages=find_packages(),
    package_data={},
    # data_files=data_files,
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    extras_require=extras_require,
    dependency_links=dependency_links,
    zip_safe=True,
    test_suite='nose.collector',
    include_package_data=True,
    entry_points={'console_scripts': ['tweemanager=tweemanager.tweemanager:tweemanager']},
    classifiers=[
        'Development Status :: Beta-rc',
        'Intended Audience :: Developers, Administrators',
        'Topic :: Text Processing :: General',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
)