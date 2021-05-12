"""Compile module."""

# Official Libraries
import yaml

# My Modules
from sms.core.aliasconv import apply_alias
from sms.core.instrunner import apply_instructions
from sms.core.nametagconv import nametags_from
from sms.core.nextconv import apply_scene_info_next
from sms.core.sameconv import apply_scene_action_same, apply_scene_info_same
from sms.core.serializer import call_scene
from sms.db.assets import AssetsDB
from sms.db.scenes import ScenesDB
from sms.db.storydata import StoryData
from sms.syss import messages as msg
from sms.syss.paths import FILE_CONFIG
from sms.utils.dicts import dict_sorted
from sms.utils.fileio import read_file
from sms.utils.log import logger


__all__ = (
        'compile_codes',
        )


# Define Constants
PROC = 'COMPILER'

ELM_CONFIG = 'config'

ELM_ENTRY = 'entrypoint'


# Main
def compile_codes(scenes: ScenesDB, assets: AssetsDB) -> StoryData:
    assert isinstance(scenes, ScenesDB)
    assert isinstance(assets, AssetsDB)

    logger.debug(msg.PROC_START.format(proc=PROC))

    config = yaml.safe_load(read_file(FILE_CONFIG))
    if not config:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"config file: {PROC}"))
        return None

    entry = config[ELM_CONFIG][ELM_ENTRY]

    if not scenes.has(entry):
        logger.error(msg.ERR_FAIL_MISSING_DATA_WITH_DATA.format(data=f"entry point: {PROC}"),
                entry)
        return None

    data = call_scene(0, entry, scenes)
    if not data:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"story data: {PROC}"))
        return None

    tags = nametags_from(assets)
    if not tags:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"name tags: {PROC}"))
        return None
    tags_sorted = dict_sorted(tags)

    updated_alias = apply_alias(data)
    if not updated_alias:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"apply alias data: {PROC}"))
        return None

    updated_same_info = apply_scene_info_same(updated_alias)
    if not updated_same_info:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"apply same info data: {PROC}"))
        return None

    updated_same_acts = apply_scene_action_same(updated_same_info)
    if not updated_same_acts:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"apply same act data: {PROC}"))
        return None

    # if date and year refine by next
    updated_next = apply_scene_info_next(updated_same_acts)
    if not updated_next:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"apply next date time: {PROC}"))
        return None

    # apply inst
    updated_inst = apply_instructions(updated_next)
    if not updated_inst:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"apply instruction data: {PROC}"))
        return None

    # tag convert
    # TODO: ここで一回タグ変換するか？いなか？
    logger.debug(msg.MSG_UNIMPLEMENT_PROC.format(proc=f"tag convert phase: {PROC}"))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return StoryData(updated_inst)


# Processes
