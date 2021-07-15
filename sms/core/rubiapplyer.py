"""Rubi apply module."""

# Official Libraries
import re


# My Modules
from sms.db.outputsdata import OutputsData
from sms.objs.rubi import Rubi, RubiData
from sms.syss import messages as msg
from sms.utils.log import logger


__all__ = (
        'apply_rubi_in_novel_data',
        )


# Define Constants
PROC = 'RUBI APPLYER'


# Main
def apply_rubi_in_novel_data(outputs: OutputsData, rubis: RubiData) -> OutputsData:
    assert isinstance(outputs, OutputsData)
    assert isinstance(rubis, RubiData)

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
    def conv_rubi(cls, text: str, rubis: RubiData) -> str:
        assert isinstance(text, str)
        assert isinstance(rubis, RubiData)

        tmp = text

        for tag, rubi in rubis.data.items():
            assert isinstance(tag, str)
            assert isinstance(rubi, Rubi)
            # match test
            if re.search(r'{}'.format(tag), tmp):
                if rubi.is_done():
                    continue
                tmp = cls._add_rubi(tmp, tag, rubi.name)
                rubi.done()

        return tmp

    def _add_rubi(src: str, key: str, rubi: str, num: int = 1) -> str:
        return re.sub(r'{}'.format(key), r'{}'.format(rubi), src, num)
