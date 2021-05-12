"""Initialize project module."""

# Official Libraries
import os


# My Modules
from sms.syss import messages as msg
from sms.syss.paths import DIR_DATA, DIR_PROJECT, DIR_BUILD_NAME
from sms.syss.paths import FILE_BOOK, FILE_CONFIG, FILE_PROJECT
from sms.syss.paths import EXT_MARKDOWN, EXT_YAML
from sms.syss.settings import APP_NAME, COPYRIGHT, VERSION
from sms.utils.fileio import read_file, write_file
from sms.utils.filepath import add_extention, basename_of, is_exists_path
from sms.utils.log import logger


__all__ = (
        'init_project',
        )


# Define Constants
PROC = 'INIT PROJECT'


DEFAULT_ASSET_DIR = 'assets'

DEFAULT_SRC_DIR = 'src'

DEFAULT_TEMP_DIR = 'temp'

DEFAULT_COMMON = 'common'

DEFAULT_ASSET_COMMON = os.path.join(DEFAULT_ASSET_DIR, DEFAULT_COMMON)

DIR_EXAMPLE = os.path.join(DIR_DATA, 'example')

DIR_COMMON = os.path.join(DIR_DATA, 'common')

DIR_TEMP = os.path.join(DIR_DATA, 'temp')

DEF_DIRS = [
        DEFAULT_ASSET_DIR,
        DEFAULT_SRC_DIR,
        DIR_BUILD_NAME,
        DEFAULT_TEMP_DIR,
        DEFAULT_ASSET_COMMON,
        ]


BASE_FILES = [
        FILE_BOOK,
        FILE_CONFIG,
        FILE_PROJECT,
        ]


COMMON_FILES = [
        'mob',
        'time',
        'word',
        'rubi',
        ]


SAMPLE_SRC = [
        'main',
        ]


SAMPLE_DATA = [
        'taro',
        'hana',
        'Classroom',
        ]


TEMP_FILES = [
        add_extention('scene', EXT_MARKDOWN),
        add_extention('person', EXT_YAML),
        add_extention('item', EXT_YAML),
        add_extention('stage', EXT_YAML),
        ]


# Main
def init_project() -> bool:

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not DirCreator.create_default_dirs():
        return False

    if not FileCreator.create_base_project_files():
        return False

    if not FileCreator.create_common_files():
        return False

    if not FileCreator.create_default_files():
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return True


# Processes
class DirCreator(object):

    @classmethod
    def create_default_dirs(cls) -> bool:

        for dirname in DEF_DIRS:
            _dirname = os.path.join(DIR_PROJECT, dirname)
            if not cls._safe_create_dir(_dirname):
                logger.warning(msg.ERR_FAIL_CANNOT_CREATE_DATA.format(data=f"{_dirname}"))
                return False

        return True

    def _safe_create_dir(dirname: str) -> bool:
        assert isinstance(dirname, str)

        if os.path.exists(dirname):
            logger.debug(msg.PROC_MESSAGE.format(proc=f"Already exists dir of {dirname}"))
            return True
        else:
            os.makedirs(dirname)
            logger.debug(msg.PROC_MESSAGE.format(proc=f"Create dir of {dirname}"))
            return True


class FileCreator(object):

    @classmethod
    def create_base_project_files(cls) -> bool:

        for path in BASE_FILES:
            if is_exists_path(path):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Already exists {path}"))
                continue

            data_path = os.path.join(DIR_DATA, basename_of(path, False))
            data = read_file(data_path)

            if path == FILE_PROJECT:
                data = cls._replace_project_file_data(data)

            if write_file(path, data):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Create {path}"))
            else:
                logger.warning(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"{path}"))
                return False

        return True

    @classmethod
    def create_common_files(cls) -> bool:

        dir_asset = os.path.join(DIR_PROJECT, DEFAULT_ASSET_DIR)
        dir_common = os.path.join(dir_asset, DEFAULT_COMMON)

        for fname in COMMON_FILES:
            _fname = add_extention(fname, EXT_YAML)
            data_path = os.path.join(DIR_COMMON, _fname)
            data = read_file(data_path)

            path = os.path.join(dir_common, _fname)
            if is_exists_path(path):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Already exists {path}"))
                continue

            if write_file(path, data):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Create {path}"))
            else:
                logger.warning(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"{path}"))
                return False

        return True

    @classmethod
    def create_default_files(cls) -> bool:

        dir_asset = os.path.join(DIR_PROJECT, DEFAULT_ASSET_DIR)
        dir_src = os.path.join(DIR_PROJECT, DEFAULT_SRC_DIR)
        dir_temp = os.path.join(DIR_PROJECT, DEFAULT_TEMP_DIR)

        for fname in SAMPLE_DATA:
            _fname = add_extention(fname, EXT_YAML)
            data_path = os.path.join(DIR_EXAMPLE, _fname)
            data = read_file(data_path)

            path = os.path.join(dir_asset, _fname)
            if is_exists_path(path):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Already exists {path}"))
                continue

            if write_file(path, data):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Create {path}"))
            else:
                logger.warning(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"{path}"))
                return False

        for fname in SAMPLE_SRC:
            _fname = add_extention(fname, EXT_MARKDOWN)
            data_path = os.path.join(DIR_EXAMPLE, _fname)
            data = read_file(data_path)

            path = os.path.join(dir_src, _fname)
            if is_exists_path(path):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Already exists {path}"))
                continue

            if write_file(path, data):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Create {path}"))
            else:
                logger.warning(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"{path}"))
                return False

        for fname in TEMP_FILES:
            data_path = os.path.join(DIR_TEMP, fname)
            data = read_file(data_path)

            path = os.path.join(dir_temp, fname)
            if write_file(path, data):
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Create {path}"))
            else:
                logger.warning(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"{path}"))
                return False

        return True

    def _replace_project_file_data(data: str) -> str:
        assert isinstance(data, str)

        return data.replace('{APPNAME}', APP_NAME).replace('{VERSION}', VERSION).replace('{COPYRIGHT}', COPYRIGHT)
