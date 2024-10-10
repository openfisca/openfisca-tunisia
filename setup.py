#! /usr/bin/env python

from setuptools import setup, find_namespace_packages
from pathlib import Path

# Read the contents of our README file for PyPi
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name = 'OpenFisca-Tunisia',
    version = '0.33.4',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.org',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    description = 'Tunisia tax and benefit system for OpenFisca',
    keywords = 'benefit tunisia microsimulation social tax',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    license_files = ('LICENSE.AGPL.txt',),
    url = 'https://github.com/openfisca/openfisca-tunisia',
    long_description=long_description,
    long_description_content_type='text/markdown',

    data_files = [
        (
            'share/openfisca/openfisca-tunisia',
            ['CHANGELOG.md', 'README.md'],
            ),
        ],
    extras_require = {
        'dev': [
            'autopep8 >=2.0.2, <3.0',
            'flake8 >=6.0.0, <7.0.0',
            'flake8-print >=5.0.0, <6.0.0',
            'flake8-quotes >=3.3.2',
            'pytest >=7.2.2, <8.0',
            'scipy >=1.10.1, <2.0',  # Only used to test de_net_a_brut reform
            'requests >=2.28.2, <3.0',
            'yamllint >=1.30.0, <2.0'
            ],
        'notebook': [
            'ipykernel >= 4.8',
            'jupyter-client >= 5.2',
            'matplotlib >= 2.2',
            'nbconvert >= 5.3',
            'nbformat >= 4.4',
            'pandas >= 0.22.0',
            ],
        'survey': [
            'OpenFisca-Survey-Manager >=0.34,<1.0',
            ],
        },
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'OpenFisca-Core >=40.0.1, <42',
        'scipy >= 0.12',
        ],
    # message_extractors = {'openfisca_tunisia': [
    #     ('**.py', 'python', None),
    #     ]},
    packages = find_namespace_packages(exclude = [
        'tests*',
        ]),
    )
