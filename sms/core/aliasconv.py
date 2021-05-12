"""Convert module for alias."""

# Official Libraries


# My Modules
from sms.objs.action import Action
from sms.objs.basecode import BaseCode
from sms.objs.instruction import Instruction
from sms.objs.sceneend import SceneEnd
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.types.instruction import InstType
from sms.utils import assertion
from sms.utils.dicts import dict_sorted
from sms.utils.log import logger
from sms.utils.strtranslate import translate_tags_str


__all__ = (
        'apply_alias',
        )


# Define Constants
PROC = 'ALIAS CONV'


# Main
def apply_alias(data: list) -> list:
    assert isinstance(data, list)

    tmp = []
    alias = []
    current = -1

    for record in data:
        assert isinstance(record, BaseCode)
        if isinstance(record, SceneInfo):
            current += 1
            alias.append({})
            tmp.append(record)
        elif isinstance(record, SceneEnd):
            current -= 1
            tmp.append(record)
        elif isinstance(record, Instruction) and InstType.ALIAS is record.type:
            tokens = assertion.is_list(record.args)
            alias[current][tokens[0]] = tokens[2]
        elif isinstance(record, Action):
            ret = TagConv.apply_alias_to_action(
                    record, dict_sorted(alias[current], True))
            tmp.append(ret)
        else:
            tmp.append(record)

    logger.debug(msg.PROC_MESSAGE.format(proc=f"completed apply alias: {PROC}"))

    return tmp


# Processes
class TagConv(object):

    def apply_alias_to_action(record: Action, alias: dict) -> Action:
        assert isinstance(record, Action)
        assert isinstance(alias, dict)

        descs = [translate_tags_str(desc, alias) for desc in record.descs]

        return Action(
                record.type,
                alias[record.subject] if record.subject in alias else record.subject,
                translate_tags_str(record.outline, alias),
                descs,
                translate_tags_str(record.note, alias),
                )
