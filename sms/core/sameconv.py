"""Convert module for same data."""

# Official Libraries


# My Modules
from sms.objs.action import Action
from sms.objs.basecode import BaseCode
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.types.action import ActType
from sms.utils.log import logger


__all__ = (
        'apply_scene_action_same',
        'apply_scene_info_same',
        )


# Define Constants
PROC = 'SAME CONV'


# Main
def apply_scene_action_same(data: list) -> list:
    assert isinstance(data, list)

    _PROC = f"{PROC}: scene action same conv"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    cache = None

    for record in data:
        assert isinstance(record, BaseCode)
        if isinstance(record, Action):
            ret = Converter.conv_same_action(record, cache)
            tmp.append(ret)
            cache = ret
        else:
            tmp.append(record)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return tmp


def apply_scene_info_same(data: list) -> list:
    assert isinstance(data, list)

    _PROC = f"{PROC}: scene info same conv"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    cache = None

    for record in data:
        assert isinstance(record, BaseCode)
        if isinstance(record, SceneInfo):
            ret = Converter.conv_same_info(record, cache)
            if ret:
                tmp.append(ret)
                cache = ret
            else:
                # nospin
                tmp.append(record)
        else:
            tmp.append(record)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return tmp


# Processes
class Converter(object):

    @classmethod
    def conv_same_action(cls, act: Action, cache: Action) -> Action:
        assert isinstance(act, Action)

        if cache:
            assert isinstance(cache, Action)
        else:
            return act

        return Action(
                cache.type if ActType.SAME is act.type else act.type,
                cache.subject if cls._is_same(act.subject) else act.subject,
                act.outline,
                act.descs,
                act.note,
                )

    @classmethod
    def conv_same_info(cls, info: SceneInfo, cache: SceneInfo) -> SceneInfo:
        assert isinstance(info, SceneInfo)

        if 'nospin' in info.flags:
            return None

        time = info.time
        if cache:
            assert isinstance(cache, SceneInfo)
        else:
            return info

        clock = info.clock

        if cls._is_same(info.time):
            time = cache.time
            clock = cache.clock

        return SceneInfo(
                info.level,
                info.tag,
                info.title,
                cache.camera if cls._is_same(info.camera) else info.camera,
                cache.stage if cls._is_same(info.stage) else info.stage,
                info.location,
                cls._is_datetime_same(info.year),
                cls._is_datetime_same(info.date),
                time,
                clock,
                info.outline,
                info.flags,
                info.note,
                )

    def _is_same(text: str) -> bool:
        assert isinstance(text, str)
        if text:
            return '-' == text
        else:
            return True

    @classmethod
    def _is_datetime_same(cls, text: str) -> str:
        assert isinstance(text, str)
        if cls._is_same(text):
            return 'same'
        else:
            return text
