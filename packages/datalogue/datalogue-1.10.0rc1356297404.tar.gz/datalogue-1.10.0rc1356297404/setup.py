
# DO NOT EDIT THIS FILE -- AUTOGENERATED BY PANTS
# Target: dtl-python-sdk:datalogue

from setuptools import setup

setup(**{
    'name': 'datalogue',
    'version': '1.10.0-RC.1356297404',
    'author': 'Nicolas Joseph',
    'author_email': 'nic@datalogue.io',
    'license': """
        Copyright 2021 Datalogue, Inc.

        This Datalogue SDK is licensed solely pursuant to the terms of the Master Software License executed between you as Licensee and Datalogue, Inc.

        All rights reserved.
        """,
    'description': 'SDK to interact with the datalogue platform',
    'long_description': '',
    'long_description_content_type': 'text/markdown',
    'url': 'https://github.com/datalogue/platform',
    'classifiers': [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    'python_requires': '>=3.6',
    'setup_requires': [
        'pytest-runner',
    ],
    'tests_require': [
        'pytest>=3.6.3',
        'pytest-cov>=2.6.0',
    ],
    'package_dir': {
        '': 'src',
    },
    'packages': [
        'datalogue',
        'datalogue.auth',
        'datalogue.clients',
        'datalogue.models',
        'datalogue.models.kinesis',
        'datalogue.models.transformations',
    ],
    'package_data': {
    },
    'install_requires': [
        'requests',
        'python-dateutil',
        'validators',
        'pytest>=3.6.3',
        'numpy>=1.19.4',
        'pyyaml',
        'pyarrow',
        'pandas>=1.1.5',
        'pbkdf2',
    ],
})
