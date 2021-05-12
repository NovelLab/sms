"""Project path utility module."""

# Official Libraries
import os

# My Modules
from sms.syss.paths import DIR_PROJECT, DIR_BUILD_NAME


__all__ = (
        'PathManager',
        )


# Define Constants
DEFAULT_ASSET_DIR = 'assets'

DEFAULT_SRC_DIR = 'src'


# Main
class PathManager(object):

    asset_dir = os.path.join(DIR_PROJECT, DEFAULT_ASSET_DIR)
    src_dir = os.path.join(DIR_PROJECT, DEFAULT_SRC_DIR)

    @classmethod
    def get_asset_dir_path(cls) -> str:
        return cls.asset_dir

    @classmethod
    def get_src_dir_path(cls) -> str:
        return cls.src_dir
