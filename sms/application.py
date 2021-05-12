"""Main Application module."""

# Official Libraries
import os
from argparse import Namespace
from enum import auto, Enum


# My Modules
from sms.cmds.builder import build_project
from sms.cmds.cmdlineparser import get_commandline_arguments
from sms.cmds.initializer import init_project
from sms.syss import messages as msg
from sms.utils.log import logger


__all__ = (
        'Application',
        )


# Define Constants
PROC = 'APPLICATION'


class BuildType(Enum):
    BUILD = auto()
    INIT = auto()

    def to_check(self) -> tuple:
        return {
                self.BUILD: ('b', 'build'),
                self.INIT: ('i', 'init')
                }[self]


# Main
class Application(object):

    def __init__(self):
        logger.debug(msg.PROC_INITIALIZED.format(proc=PROC))

    def run(self) -> int:
        logger.debug(msg.PROC_START.format(proc=PROC))

        args = get_commandline_arguments()
        if not args:
            logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"command line args: {PROC}"))
            return os.EX_NOINPUT

        if BuildChecker.has_build_cmd_of(args, BuildType.BUILD):
            if not build_project(args):
                logger.debug(msg.ERR_FAIL_SUBPROCESS.format(proc=f"build project: {PROC}"))
                return os.EX_SOFTWARE
        elif BuildChecker.has_build_cmd_of(args, BuildType.INIT):
            if not init_project():
                logger.debug(msg.ERR_FAIL_SUBPROCESS.format(proc=f"init project: {PROC}"))
                return os.EX_SOFTWARE
        else:
            logger.warning(
                    msg.ERR_FAIL_INVALID_DATA_WITH_DATA.format(data=f"build command: {PROC}"),
                    args.cmd)
            return os.EX_NOINPUT

        logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
        return os.EX_OK


# Processes
class BuildChecker(object):

    def has_build_cmd_of(args: Namespace, type: BuildType) -> bool:
        assert isinstance(args, Namespace)
        assert isinstance(type, BuildType)

        return args.cmd in type.to_check()
