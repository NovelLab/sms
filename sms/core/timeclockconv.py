"""Time and clock convert module."""

# Official Libraries


# My Modules
from sms.objs.basecode import BaseCode
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.utils.log import logger


__all__ = (
        'apply_scene_time_to_clock',
        )


# Define Constants
PROC = 'TIME CLOCK CONV'


# Main
def apply_scene_time_to_clock(data: list, timeclocks: dict) -> list:
    assert isinstance(data, list)
    assert isinstance(timeclocks, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []

    for record in data:
        assert isinstance(record, BaseCode)
        if isinstance(record, SceneInfo):
            ret = Converter.time_to_clock_in_scene(record, timeclocks)
            if ret:
                tmp.append(ret)
            else:
                tmp.append(record)
        else:
            tmp.append(record)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return tmp


# Processes
class Converter(object):

    def time_to_clock_in_scene(info: SceneInfo, timeclocks: dict) -> SceneInfo:
        assert isinstance(info, SceneInfo)
        assert isinstance(timeclocks, dict)

        time = info.time
        clock = info.clock

        if clock and ':' in clock:
            return info

        if time in timeclocks:
            return SceneInfo(
                    info.level,
                    info.tag,
                    info.title,
                    info.camera,
                    info.stage,
                    info.location,
                    info.year,
                    info.date,
                    info.time,
                    timeclocks[time],
                    info.outline,
                    info.flags,
                    info.note,
                    )
        else:
            return info
