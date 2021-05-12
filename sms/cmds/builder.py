"""Build module."""

# Official Libraries
import os
import yaml
from argparse import Namespace
from enum import auto, Enum


# My Modules
from sms.core.charcounter import char_counts_from
from sms.core.compiler import compile_codes
from sms.core.contentsbuilder import build_contents
from sms.core.dbmanager import get_assets_db, get_srcs_db
from sms.core.dbmanager import scenes_db_from
from sms.core.infobuilder import build_info
from sms.core.nametagconv import nametags_from, callingtags_from
from sms.core.nametagconv import rubitags_from
from sms.core.novelbuilder import build_novel
from sms.core.outlinebuilder import build_outline
from sms.core.plotbuilder import build_plot
from sms.core.rubiapplyer import apply_rubi_in_novel_data
from sms.core.scriptbuilder import build_script
from sms.core.structbuilder import build_struct
from sms.db.assets import AssetsDB
from sms.db.scenes import ScenesDB
from sms.db.outputsdata import OutputsData
from sms.db.srcs import SrcsDB
from sms.syss import messages as msg
from sms.syss.paths import DIR_PROJECT, DIR_BUILD_NAME, EXT_MARKDOWN
from sms.syss.paths import FILE_CONFIG
from sms.types.build import BuildType
from sms.utils.fileio import read_file, write_file
from sms.utils.filepath import add_extention, is_exists_path
from sms.utils.log import logger


__all__ = (
        'build_project',
        )


# Define Constants
PROC = 'BUILD PROJECT'


# Main
def build_project(args: Namespace) -> bool:
    assert isinstance(args, Namespace)

    logger.debug(msg.PROC_START.format(proc=PROC))

    assets = get_assets_db()
    if not assets or assets.is_empty():
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"assets db: {PROC}"))
        return False

    builds = {
            BuildType.OUTLINE: None,
            BuildType.PLOT: None,
            BuildType.SCRIPT: None,
            BuildType.NOVEL: None,
            }

    srcs = get_srcs_db()
    if not srcs or srcs.is_empty():
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"srcs db: {PROC}"))
        return False

    scenes = scenes_db_from(srcs)
    if not scenes or scenes.is_empty():
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"scenes db: {PROC}"))
        return False

    codes = compile_codes(scenes, assets)
    if not codes:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"story data: {PROC}"))
        return False

    logger.debug(msg.MSG_UNIMPLEMENT_PROC.format(proc=PROC))

    nametags = nametags_from(assets)
    callings = callingtags_from(assets)
    is_comment = args.comment

    contents = build_contents(codes, nametags)
    if not contents:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"contents data: {PROC}"))
        return False

    if Checker.has(args, BuildType.OUTLINE):
        outputs = build_outline(codes, nametags)
        if not outputs or outputs.is_empty():
            logger.error(
                    msg.ERR_FAIL_MISSING_DATA.format(data=f"outline output data: {PROC}"))
            return False

        builds[BuildType.OUTLINE] = outputs

        if not Outputter.output_data(_get_build_path('outline'),
                contents.cloned() + outputs):
            logger.error(
                    msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"output outline data: {PROC}"))
            return False

    if Checker.has(args, BuildType.PLOT):
        outputs = build_plot(codes, nametags)
        if not outputs or outputs.is_empty():
            logger.error(
                    msg.ERR_FAIL_MISSING_DATA.format(data=f"plot output data: {PROC}"))
            return False

        builds[BuildType.PLOT] = outputs

        if not Outputter.output_data(_get_build_path('plot'),
                contents.cloned() + outputs):
            logger.error(
                    msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"output plot data: {PROC}"))
            return False

    if Checker.has(args, BuildType.STRUCT):
        outputs = build_struct(codes, nametags, callings, is_comment)
        if not outputs or outputs.is_empty():
            logger.error(
                    msg.ERR_FAIL_MISSING_DATA.format(data=f"struct output data: {PROC}"))
            return False

        if not Outputter.output_data(_get_build_path('struct'),
                contents.cloned() + outputs):
            logger.error(
                    msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"output struct data: {PROC}"))
            return False

    if Checker.has(args, BuildType.SCRIPT):
        outputs = build_script(codes, nametags, callings, is_comment)
        if not outputs or outputs.is_empty():
            logger.error(
                    msg.ERR_FAIL_MISSING_DATA.format(data=f"script output data: {PROC}"))
            return False

        builds[BuildType.SCRIPT] = outputs

        if not Outputter.output_data(_get_build_path('script'),
                contents.cloned() + outputs):
            logger.error(
                    msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"output script data: {PROC}"))
            return False

    if Checker.has(args, BuildType.NOVEL):
        outputs = build_novel(codes, nametags, callings, is_comment)
        if not outputs or outputs.is_empty():
            logger.error(
                    msg.ERR_FAIL_MISSING_DATA.format(data=f"novel output data: {PROC}"))
            return False

        builds[BuildType.NOVEL] = outputs

        if not Outputter.output_data(_get_build_path('novel'),
                contents.cloned() + outputs):
            logger.error(
                    msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"output novel data: {PROC}"))
            return False

        if args.rubi:
            outputs_rubi = outputs.cloned()
            rubis = rubitags_from(assets)
            updated_rubi = apply_rubi_in_novel_data(outputs_rubi, rubis)

            if not Outputter.output_data(_get_build_ipath('novel_rubi'),
                    contents.cloned() + updated_rubi):
                logger.error(
                        msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"output novel with rubi data: {PROC}"))
                return False

    if Checker.has(args, BuildType.INFO):
        outputs = build_info(codes, nametags, callings)
        if not outputs or outputs.is_empty():
            logger.debug(msg.ERR_FAIL_MISSING_DATA.format(data=f"info output data: {PROC}"))
            return False

        if not Outputter.output_data(_get_build_path('info'),
                outputs):
            logger.error(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"output info data: {PROC}"))
            return False

    if not BaseInfoBuilder.build_base_info(args, builds):
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"base info outputs: {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return True


# Processes
class Checker(object):

    def has(args: Namespace, type: BuildType) -> bool:
        assert isinstance(args, Namespace)
        assert isinstance(type, BuildType)

        if BuildType.OUTLINE is type:
            return args.outline
        elif BuildType.PLOT is type:
            return args.plot
        elif BuildType.SCRIPT is type:
            return args.script
        elif BuildType.NOVEL is type:
            return args.novel
        elif BuildType.STRUCT is type:
            return args.struct
        elif BuildType.INFO is type:
            return args.info
        else:
            return False


class BaseInfoBuilder(object):

    @classmethod
    def build_base_info(cls, args: Namespace, outputs_data: dict) -> bool:
        assert isinstance(args, Namespace)
        assert isinstance(outputs_data, dict)

        tmp = OutputsData(['BASE INFO\n===\n\n'])
        columns, rows = _get_columns_and_rows()

        for type, outputs in outputs_data.items():
            if Checker.has(args, type) and outputs:
                assert isinstance(outputs, OutputsData)
                ret = char_counts_from(type, outputs.get_data(), columns, rows)
                if ret:
                    tmp += OutputsData(ret)

        if not tmp or tmp.is_empty():
            logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"base info data: {PROC}"))
            return False

        if not Outputter.output_data(_get_build_path('base'), tmp):
            logger.error(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"base info data: {PROC}"))
            return False

        logger.debug(msg.PROC_MESSAGE.format(proc=f"ouputted base infos: {PROC}"))

        return True


class Outputter(object):

    def output_data(path: str, outputs: OutputsData) -> bool:
        assert isinstance(path, str)
        assert isinstance(outputs, OutputsData)

        if not write_file(path, outputs.get_serialized_data()):
            logger.warning(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"outputs data to {path}: {PROC}"))
            return False

        logger.debug(msg.PROC_MESSAGE.format(proc=f"write {path}"))
        return True


# Private Functions
def _get_build_path(fname: str) -> str:
    assert isinstance(fname, str)

    dir_name = os.path.join(DIR_PROJECT, DIR_BUILD_NAME)
    return os.path.join(dir_name, add_extention(fname, EXT_MARKDOWN))


def _get_columns_and_rows() -> tuple:
    data = yaml.safe_load(read_file(FILE_CONFIG))['config']
    return data['columns'], data['rows']
