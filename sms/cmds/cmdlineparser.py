"""Parser of commandline arguments."""

# Official Libraries
from argparse import ArgumentParser, Namespace


# My Modules
from sms import __app_name__
from sms.syss import messages as msg
from sms.utils import assertion
from sms.utils.log import logger


__all__ = (
        'get_commandline_arguments',
        )


# Define Constants
PROC = 'COMMANDLINE ARG PARSER'
"""str: main process name."""

PROGRAM_NAME = __app_name__
"""str: program name for argument parser."""

DESCRIPTION = 'story building utility tool on cui.'
"""str: description for argument parser."""


# Main
def get_commandline_arguments() -> Namespace:

    logger.debug(msg.PROC_START.format(proc=PROC))

    parser = assertion.is_instance(_init_commandline_parser(),
            ArgumentParser)

    if not parser:
        logger.error(msg.ERR_FAIL_CANNOT_CREATE_DATA.format(data=f"parser: {PROC}"))
        return None

    if not _set_parser_options(parser):
        logger.warning(msg.ERR_FAIL_CANNOT_CREATE_DATA.format(data=f"arg parser options: {PROC}"))
        return None

    args = parser.parse_args()

    if not args:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"args: {PROC}"))
        return None

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return args


# Private Functions
def _init_commandline_parser() -> ArgumentParser:

    _PROC = f"{PROC}: init commandline parser"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    parser = ArgumentParser(
            prog=PROGRAM_NAME,
            description=DESCRIPTION,
            )

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return parser


def _set_parser_options(parser: ArgumentParser) -> bool:
    assert isinstance(parser, ArgumentParser)

    _PROC = f"{PROC}: set parser options"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    parser.add_argument('cmd', metavar='command', type=str, help='builder command')
    parser.add_argument('-o', '--outline', help='outline output', action='store_true')
    parser.add_argument('-p', '--plot', help='plot output', action='store_true')
    parser.add_argument('-i', '--info', help='scene info output', action='store_true')
    parser.add_argument('-u', '--status', help='status info output', action='store_true')
    parser.add_argument('-t', '--struct', help='struct output', action='store_true')
    parser.add_argument('-s', '--script', help='script output', action='store_true')
    parser.add_argument('-n', '--novel', help='novel output', action='store_true')
    parser.add_argument('-r', '--rubi', help='output with rubi', action='store_true')
    parser.add_argument('-v', '--version', help='output app version', action='store_true')
    parser.add_argument('-e', '--edit', help='add and edit when new file', action='store_true')
    parser.add_argument('--part', type=str, help='select ouput part')
    parser.add_argument('--comment', help='show comment', action='store_true')
    parser.add_argument('--debug', help='set debug flag', action='store_true')
    parser.add_argument('--debugdetail', help='set detal debug output', action='store_true')

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return True
