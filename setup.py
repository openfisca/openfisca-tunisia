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
    version = '0.10.0',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [classifier for classifier in classifiers.split('\n') if classifier],
    description = doc_lines[0],
    keywords = 'benefit microsimulation social tax tunisia',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description = '\n'.join(doc_lines[2:]),
    url = 'https://github.com/openfisca/openfisca-tunisia',

    data_files = [
        ('share/locale/ar/LC_MESSAGES', ['openfisca_tunisia/i18n/fr/LC_MESSAGES/openfisca-tunisia.mo']),
        ('share/locale/fr/LC_MESSAGES', ['openfisca_tunisia/i18n/fr/LC_MESSAGES/openfisca-tunisia.mo']),
        ],
    extras_require = dict(
        tests = [
            'nose',
            ],
        ),
    install_requires = [
        'Babel >= 0.9.4',
        'OpenFisca-Core >= 14.0.1, < 15.0',
        'PyYAML >= 3.10',
        'scipy >= 0.12',
        ],
    message_extractors = {'openfisca_tunisia': [
        ('**.py', 'python', None),
        ]},
    packages = find_packages(exclude=['openfisca_tunisia.tests*']),
    )
