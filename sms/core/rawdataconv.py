"""Raw source data convert module."""

# Official Libraries
import copy


# My Modules
from sms.objs.rawsrc import RawSrc
from sms.syss import messages as msg
from sms.utils.log import logger
from sms.utils.strings import rid_rn


__all__ = (
        'raw_src_object_from',
        )


# Define Constants
PROC = 'RAW DATA CONV'


# Main
def raw_src_objects_from(data: str) -> list:
    assert isinstance(data, str)

    logger.debug(msg.PROC_START.format(proc=PROC))

    srcs = []
    tmp = []
    current = 'global'

    for line in data.split('\n'):
        if line.startswith('#!SMS'):
            # meta mark
            continue
        elif line.startswith('## '):
            if tmp:
                srcs.append(Converter.to_src(current, copy.deepcopy(tmp)))
            current = _get_scene_tag(line)
            tmp = []
        elif line:
            tmp.append(line)
        else:
            # break line
            continue
    if tmp:
        srcs.append(Converter.to_src(current, copy.deepcopy(tmp)))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return srcs


# Processes
class Converter(object):

    def to_src(tag: str, data: list) -> RawSrc:
        assert isinstance(tag, str)
        assert isinstance(data, list)

        return RawSrc(tag, data)


# Private Functions
def _get_scene_tag(line: str) -> str:
    assert isinstance(line, str)
    assert line.startswith('## ')

    return rid_rn(line[3:])
