#!/usr/bin/env python3

# standards
from pathlib import Path
import re
import setuptools


LONG_DESCRIPTION = (Path(__file__).parent / 'README.md').read_text('UTF-8')


_version_match = re.search(
    r"KLON_VERSION = \'(.+)\'",
    (Path(__file__).parent / 'klon' / 'version.py').read_text('UTF-8'),
)
if not _version_match:
    raise ValueError('Version not found')
KLON_VERSION = _version_match.group(1)


setuptools.setup(
    name='klon',
    version=KLON_VERSION,
    author='Hervé Saint-Amand',
    author_email='klon@saintamh.org',
    description='Utilities for building and manipulating ElementTrees',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/saintamh/klon/',
    packages=setuptools.find_packages(),
    package_data={'klon': ['py.typed']},
    install_requires=[
        'lxml>=4,<5',
        'lxml-stubs>=0.1,<0.2',  # so that users can type-check their calls to Klon
        'requests>=2.25,<3',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    zip_safe=False,  # https://mypy.readthedocs.io/en/latest/installed_packages.html#creating-pep-561-compatible-packages
)
