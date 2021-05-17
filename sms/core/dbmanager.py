"""DB management module."""

# Official Libraries


# My Modules
from sms.commons.pathmanager import PathManager as PM
from sms.core.assetdataconv import asset_object_from
from sms.core.rawdataconv import raw_src_objects_from
from sms.core.scenecodeconv import scene_code_object_from
from sms.db.assets import AssetsDB
from sms.db.scenes import ScenesDB
from sms.db.srcs import SrcsDB
from sms.objs.baseobject import SObject
from sms.objs.rawsrc import RawSrc
from sms.objs.scenecode import SceneCode
from sms.syss.paths import EXT_MARKDOWN, EXT_YAML
from sms.syss import messages as msg
from sms.utils import assertion
from sms.utils.fileio import read_file
from sms.utils.filepath import get_filepaths_in, is_exists_path
from sms.utils.log import logger


__all__ = (
        'get_assets_db',
        )


# Define Constants
PROC = 'DB MANAGER'


# Main
def get_assets_db() -> AssetsDB:

    _PROC = f"{PROC}: get assets db"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    db = AssetsDB()

    paths = get_filepaths_in(PM.get_asset_dir_path(), EXT_YAML, True)

    for path in paths:

        if not is_exists_path(path):
            logger.warning(msg.ERR_FAIL_MISSING_DATA.format(data=f"asset data of {path}: {PROC}"))
            continue

        data = read_file(path)
        # NOTE: file validate?
        obj = asset_object_from(data)
        if obj:
            assert isinstance(obj, SObject)
            db.add(obj.tag, obj)
            logger.debug(msg.PROC_MESSAGE.format(proc=f"Add '{obj.tag}' to asset db"))

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return db


def get_srcs_db() -> SrcsDB:

    _PROC = f"{PROC}: get sources db"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    db = SrcsDB()

    paths = get_filepaths_in(PM.get_src_dir_path(), EXT_MARKDOWN, True)

    for path in paths:

        if not is_exists_path(path):
            logger.warning(msg.ERR_FAIL_MISSING_DATA.format(data=f"source data of {path}: {PROC}"))
            continue

        data = read_file(path)
        raws = assertion.is_list(raw_src_objects_from(data))
        for raw in raws:
            if raw:
                assert isinstance(raw, RawSrc)
                db.add(raw.tag, raw)
                logger.debug(msg.PROC_MESSAGE.format(proc=f"Add '{raw.tag}' to srcs db"))

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return db


def scenes_db_from(srcs: SrcsDB) -> ScenesDB:
    assert isinstance(srcs, SrcsDB)

    _PROC = f"{PROC}: conv scenes db from srcs db"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    db = ScenesDB()

    for tag, src in srcs.data.items():
        assert isinstance(tag, str)
        assert isinstance(src, RawSrc)
        code = scene_code_object_from(src)

        if code:
            assert isinstance(code, SceneCode)
            db.add(code.tag, code)
            logger.debug(msg.PROC_MESSAGE.format(proc=f"Add '{code.tag}' to scenes db"))

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return db
