"""Scene code convert moduler."""

# Official Libraries
from typing import Union
import re


# My Modules
from sms.objs.action import Action
from sms.objs.basecode import BaseCode
from sms.objs.instruction import Instruction
from sms.objs.rawsrc import RawSrc
from sms.objs.scenecode import SceneCode
from sms.syss import messages as msg
from sms.types.action import ActType, FLAG_ACTS, NO_SUBJECT_ACTS
from sms.types.instruction import InstType
from sms.utils.log import logger
from sms.utils.strings import rid_rn


__all__ = (
        'scene_code_object_from',
        )


# Define Constants
PROC = 'SCENE CODE CONV'


ACT_CODE = Union[Action, Instruction]

PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9]*:')


# Main
def scene_code_object_from(raw: RawSrc) -> SceneCode:
    assert isinstance(raw, RawSrc)

    logger.debug(msg.PROC_START.format(proc=PROC))

    code = SceneCode(raw.tag)
    current_act = None

    def _store_act(scode: SceneCode, act):
        assert isinstance(scode, SceneCode)
        if act:
            assert isinstance(act, (Action, Instruction))
            scode.add(act.cloned())
        return None

    for line in raw.data:
        assert isinstance(line, str)
        if line.startswith('<'):
            ret = Converter.to_call_scene(line)
            if ret:
                current_act = _store_act(code, current_act)
                code.add(ret)
        elif line.startswith('::'):
            # member
            member, val = _get_member_tokens(line)
            if not member:
                logger.warning(msg.ERR_FAIL_MISSING_DATA.format(data=f"member:'{member}' and val: '{val}' : {PROC}"))
                continue
            if hasattr(code, member):
                setattr(code, member, val)
            else:
                logger.warning(
                        msg.ERR_FAIL_INVALID_DATA_WITH_DATA.format(data=f"scene member: {PROC}"),
                        member)
        elif line.startswith('!'):
            # instruction
            ret = Converter.to_instruction(line)
            if ret:
                current_act = _store_act(code, current_act)
                code.add(ret)
        elif line.startswith('['):
            # action
            current_act = _store_act(code, current_act)
            current_act = Converter.to_action(line)
        elif line:
            # text
            if current_act:
                current_act.add(line)
        else:
            continue

    current_act = _store_act(code, current_act)

    updated_code = Restructor.restruct_dialogue_actions(code)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return updated_code


# Process
class Converter(object):

    @classmethod
    def to_action(cls, line: str) -> Action:
        assert isinstance(line, str)

        act, subject, outline = '', '', ''
        base = rid_rn(line)[1:-1]

        if ':' in base:
            tokens = base.split(':')
            if len(tokens) == 3:
                subject, act, outline = tokens[0], tokens[1], tokens[2]
            elif len(tokens) == 2:
                subject, act = tokens[0], tokens[1]
                if cls._is_special_act(subject):
                    outline = act
                    act = subject
                    subject = ''
            else:
                act = tokens[0]
        else:
            act = base
        return Action(_act_type_of(act), subject, outline)

    def to_call_scene(line: str) -> Instruction:
        assert isinstance(line, str)

        tag = rid_rn(line)[1:-1]

        return Instruction(InstType.CALL, [tag], '')

    def to_instruction(line: str) -> Instruction:
        assert isinstance(line, str)
        assert line.startswith('!')

        _line = line[1:]

        if _line.startswith(' ') and ' = ' in _line:
            # alias
            tokens = _line[1:].split(' ')
            return Instruction(InstType.ALIAS, tokens, '')
        elif _line.startswith('PE'):
            return Instruction(InstType.PARAGRAPH_END)
        elif _line.startswith('P'):
            return Instruction(InstType.PARAGRAPH_START)
        else:
            return None

    def _is_special_act(act: str) -> bool:
        assert isinstance(act, str)

        for check in FLAG_ACTS + NO_SUBJECT_ACTS:
            if act in check.to_checker():
                return True

        else:
            return False


class Restructor(object):

    @classmethod
    def restruct_dialogue_actions(cls, scode: SceneCode) -> SceneCode:
        assert isinstance(scode, SceneCode)

        tmp = []

        for record in scode.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, Action):
                if ActType.TALK is record.type:
                    ret = cls.devided_talk_acts(record)
                    if ret:
                        tmp.extend(ret)
                    else:
                        tmp.append(record)
                else:
                    tmp.append(record)
            else:
                tmp.append(record)

        return scode.replace(tmp)

    @classmethod
    def devided_talk_acts(cls, action: Action) -> list:
        assert isinstance(action, Action)
        assert ActType.TALK is action.type

        if not cls._has_other_dialogue(action.descs):
            return None

        tmp = []

        for desc in action.descs:
            assert isinstance(desc, str)
            if desc.startswith(':'):
                tmp.append(action.inherited(descs=[desc[1:]]))
            elif re.search(PATTERN, desc):
                match = re.search(PATTERN, desc).group()
                subject = match[0:-1]
                tmp.append(action.inherited(
                    subject=subject,
                    descs=[desc[len(match):]]))
            else:
                tmp.append(action.inherited(type=ActType.DO, descs=[desc]))
        return tmp

    def _has_other_dialogue(descs: list) -> bool:
        assert isinstance(descs, list)

        for desc in descs:
            assert isinstance(desc, str)
            if re.search(PATTERN, desc):
                return True
        return False


# Private Functions
def _act_type_of(tag: str) -> ActType:
    assert isinstance(tag, str)

    for act in ActType:
        if tag in act.to_checker():
            return act
    if tag:
        logger.warning(
                msg.ERR_FAIL_UNKNOWN_DATA_WITH_DATA.format(
                    data=f"act type string: {PROC}"),
                tag)
        return ActType.NONE
    else:
        return ActType.SAME


def _get_member_tokens(line: str) -> tuple:
    assert isinstance(line, str)
    assert line.startswith('::')
    assert '=' in line

    if ' ' in line:
        # 空白を含む
        tokens = rid_rn(line[2:]).split(' ')
        if tokens[1] == '=':
            if len(tokens) > 3:
                return tokens[0], ' '.join(tokens[2:])
            else:
                return tokens[0], tokens[2]
        else:
            return None, None
    else:
        # 含まない
        tokens = rid_rn(line[2:]).split('=')
        if len(tokens) >= 3:
            return tokens[0], '='.join(tokens[1:])
        else:
            return tokens[0], tokens[1]
