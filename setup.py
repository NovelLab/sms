#!/usr/bin/env python3
from setuptools import setup, find_packages

from sms import __version__ as VERSION
from sms import __app_name__ as APP_NAME

# Define constants
PACKAGE_NAME = APP_NAME
LICENSE = 'MIT'
AUTHOR = 'N.T.WORKS'
EMAIL = 'nagisc007@yahoo.co.jp'
SHORT_DESCRIPTION = 'Helper application to build your story'
LONG_DESCRITPYION = """StoryBuilder is the helper application that build your story, novel, screenplay or game scripts.
"""

setup(
        name=PACKAGE_NAME,
        version=VERSION,
        license=LICENSE,
        author=AUTHOR,
        author_email=EMAIL,
        scripts=['bin/sms'],
        install_requires=[
            "PyYAML",
        ],
        description=SHORT_DESCRIPTION,
        long_description=LONG_DESCRITPYION,
        package_data={'sms': ['data/*.yml', 'data/*.md']},
        packages=find_packages(),
        tests_require=['pytest'],
)
