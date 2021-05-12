"""Define common paths."""

# Official Libraries
import os


# My Modules
from sms import __app_base_dir__
from sms import __project_path__


# Main
EXT_MARKDOWN = 'md'
"""str: extention of markdown file."""


EXT_TEXT = 'txt'
"""str: extention of text file."""


EXT_YAML = 'yml'
"""str: extention of yaml file."""


DIR_PROJECT = __project_path__
"""str: directory path of project."""


DIR_APP = __app_base_dir__
"""str: directory path of this application."""


DIR_BUILD_NAME = 'build'
"""str: directory name for build files."""


DIR_DATA = os.path.join(DIR_APP, 'data')
"""str: directory path of data."""


FILE_PROJECT = os.path.join(DIR_PROJECT, 'project.' + EXT_YAML)
"""str: file name of project."""


FILE_BOOK = os.path.join(DIR_PROJECT, 'book.' + EXT_YAML)
"""str: file name of book."""


FILE_CONFIG = os.path.join(DIR_PROJECT, 'config.' + EXT_YAML)
"""str: file name of config."""
