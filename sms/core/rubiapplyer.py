"""Rubi apply module."""

# Official Libraries
import re


# My Modules
from sms.db.outputsdata import OutputsData
from sms.objs.rubi import Rubi
from sms.syss import messages as msg
from sms.utils.log import logger


__all__ = (
        'apply_rubi_in_novel_data',
        )


# Define Constants
PROC = 'RUBI APPLYER'


# Main
def apply_rubi_in_novel_data(outputs: OutputsData, rubis: dict) -> OutputsData:
    assert isinstance(outputs, OutputsData)
    assert isinstance(rubis, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []

    for record in outputs.get_data():
        assert isinstance(record, str)
        tmp.append(Converter.conv_rubi(record, rubis))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return OutputsData(tmp)


# Processes
class Converter(object):

    @classmethod
    def conv_rubi(cls, text: str, rubis: dict) -> str:
        assert isinstance(text, str)
        assert isinstance(rubis, dict)

        tmp = text

        for tag, rubi in rubis.items():
            assert isinstance(tag, str)
            assert isinstance(rubi, Rubi)
            # TODO: always

            tmp = cls._add_rubi(tmp, tag, rubi.name)

        return tmp

    def _add_rubi(src: str, key: str, rubi: str, num: int = 1) -> str:
        return re.sub(r'{}'.format(key), r'{}'.format(rubi), src, num)
