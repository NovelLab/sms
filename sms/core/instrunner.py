"""Instruction running module."""

# Official Libraries


# My Modules
from sms.objs.basecode import BaseCode
from sms.syss import messages as msg
from sms.utils.log import logger


__all__ = (
        'apply_instructions',
        )


# Define Constants
PROC = 'INST RUNNER'


# Main
def apply_instructions(base_data: list) -> list:
    assert isinstance(base_data, list)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []

    for record in base_data:
        assert isinstance(record, BaseCode)
        tmp.append(record)

    logger.debug(msg.MSG_UNIMPLEMENT_PROC.format(proc=PROC))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return tmp
