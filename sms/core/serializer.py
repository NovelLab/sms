"""Serialize module."""

# Official Libraries


# My Modules
from sms.db.scenes import ScenesDB
from sms.objs.action import Action
from sms.objs.instruction import Instruction
from sms.objs.scenecode import SceneCode
from sms.objs.sceneend import SceneEnd
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.types.instruction import InstType
from sms.utils import assertion
from sms.utils.log import logger


__all__ = (
        'call_scene',
        )


# Define Constants
PROC = 'SERIALIZER'


# Main
def call_scene(level: int, tag: str, scenes: ScenesDB) -> list:
    assert isinstance(level, int)
    assert isinstance(tag, str)
    assert isinstance(scenes, ScenesDB)

    if not scenes.has(tag):
        logger.warning(
                msg.ERR_FAIL_MISSING_DATA_WITH_DATA.format(data=f"call tag: {PROC}"),
                tag)
        return []

    tmp = []

    scode = assertion.is_instance(scenes.get(tag), SceneCode)
    tmp.append(Converter.conv_scene_info_from(level, scode))

    for obj in scode.data:
        if isinstance(obj, Action):
            tmp.append(obj)
        elif isinstance(obj, Instruction):
            if InstType.CALL is obj.type:
                call_tag = obj.args[0]
                # TODO: 親タグも取得して相互呼び出しを禁止する
                if tag == call_tag:
                    logger.error(
                            msg.ERR_FAIL_MUSTBE_WITH_DATA.format(data=f"not self calling: {PROC}"),
                            tag)
                    raise ValueError('invalid self calling', tag)
                ret = call_scene(level + 1, obj.args[0], scenes)
                if ret:
                    tmp.extend(ret)
            else:
                tmp.append(obj)
        else:
            logger.warning(
                    msg.ERR_FAIL_INVALID_DATA_WITH_DATA.format(data=f"scene code object: {PROC}"),
                    obj)
            continue
    tmp.append(_get_scene_end(scode))

    return tmp


# Processes
class Converter(object):

    @classmethod
    def conv_scene_info_from(cls, level: int, scode: SceneCode) -> SceneInfo:
        assert isinstance(level, int)
        assert isinstance(scode, SceneCode)

        return SceneInfo(
                level,
                scode.tag,
                scode.title,
                scode.camera,
                scode.stage,
                scode.location,
                scode.year,
                scode.date,
                scode.time,
                scode.time if scode.time and ':' in scode.time else '-',
                scode.outline,
                scode.flags,
                scode.note,
                )


# Private Functions
def _get_scene_end(scode: SceneCode) -> SceneEnd:
    assert isinstance(scode, SceneCode)

    return SceneEnd(scode.tag)
