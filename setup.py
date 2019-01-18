#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Tunisia specific model for OpenFisca -- a versatile microsimulation free software"""


from setuptools import setup, find_packages


classifiers = """\
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: POSIX
Programming Language :: Python
Topic :: Scientific/Engineering :: Information Analysis
"""

doc_lines = __doc__.split('\n')


setup(
    name = 'OpenFisca-Tunisia',
    version = '0.21.1',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.org',
    classifiers = [classifier for classifier in classifiers.split('\n') if classifier],
    description = doc_lines[0],
    keywords = 'benefit microsimulation social tax tunisia',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description = '\n'.join(doc_lines[2:]),
    url = 'https://github.com/openfisca/openfisca-tunisia',

    data_files = [
        ('share/openfisca/openfisca-tunisia', ['CHANGELOG.md', 'LICENSE.AGPL.txt', 'README.md']),
        ],
    extras_require = dict(
        tests = [
            'nose >= 1.3.7'
            ],
        notebook = [
            'ipykernel >= 4.8',
            'jupyter-client >= 5.2',
            'matplotlib >= 2.2',
            'nbconvert >= 5.3',
            'nbformat >= 4.4',
            'pandas >= 0.22.0',
            ],
        survey = [
            'OpenFisca-Survey-Manager >= 0.9.5, < 0.10',
            ]
        ),
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'OpenFisca-Core >=24,<26',
        'PyYAML >= 3.10',
        'scipy >= 0.12',
        ],
    message_extractors = {'openfisca_tunisia': [
        ('**.py', 'python', None),
        ]},
    packages = find_packages(exclude=['tests*', 'old_tests*']),
    )
