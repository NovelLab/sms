"""Build script module."""

# Official Libraries
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Any


# My Modules
from sms.commons.format import get_br, get_indent
from sms.commons.format import join_descs, markdown_comment_style_of
from sms.db.outputsdata import OutputsData
from sms.db.storydata import StoryData
from sms.objs.action import Action
from sms.objs.basecode import BaseCode
from sms.objs.instruction import Instruction
from sms.objs.sceneend import SceneEnd
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.types.action import ActType
from sms.types.instruction import InstType
from sms.utils import assertion
from sms.utils.log import logger
from sms.utils.strtranslate import translate_tags_str
from sms.utils.strtranslate import translate_tags_text_list


__all__ = (
        'build_script',
        )


# Define Constants
PROC = 'BUILD SCRITP'


class RecordType(Enum):
    NONE = auto()
    # base
    DESCRIPTION = auto()
    DIALOGUE = auto()
    MONOLOGUE = auto()
    VOICE = auto()
    # effect
    SE = auto()
    # symbol
    BR = auto()
    SYMBOL = auto()
    TITLE = auto()
    # scene data
    SPIN = auto()
    SCENE_END = auto()
    # others
    NOTE = auto()


NORMAL_DESCS = [
        RecordType.DESCRIPTION,
        RecordType.DIALOGUE,
        RecordType.MONOLOGUE,
        RecordType.VOICE,
        ]


@dataclass
class SpinInfo(object):
    subject: str
    stage: str
    year: str
    date: str
    time: str
    clock: str


@dataclass
class ScriptRecord(object):
    type: RecordType
    subject: str
    descs: list = field(default_factory=list)
    note: Any = None


# Main
def build_script(story_data: StoryData, tags: dict, callings: dict,
        is_comment: bool) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(callings, dict)
    assert isinstance(is_comment, bool)

    logger.debug(msg.PROC_START.format(proc=PROC))

    scripts = Converter.scripts_data_from(story_data)
    if not scripts:
        return None

    updated_tags = TagConverter.conv_callings_and_tags(scripts, tags, callings)
    if not updated_tags:
        return None

    formatted = Formatter.format_data(updated_tags, is_comment)
    if not formatted:
        return None

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return OutputsData(translated)


# Processes
class Converter(object):

    @classmethod
    def scripts_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []
        indices = [0]

        for record in story_data.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, SceneInfo):
                if record.level >= len(indices):
                    indices.append(0)
                indices[record.level] += 1
                ret = cls._to_scene_head(indices[record.level], record)
                if ret:
                    tmp.append(ret)
                ret = cls._to_scene_spin(record)
                if ret:
                    tmp.append(ret)
            elif isinstance(record, SceneEnd):
                tmp.append(cls._get_scene_end())
            elif isinstance(record, Action):
                ret = cls._to_scene_act(record)
                if ret:
                    tmp.append(ret)
            elif isinstance(record, Instruction):
                ret = cls._to_scene_control(record)
                if ret:
                    tmp.append(ret)
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted script data: {PROC}"))

        return tmp

    @classmethod
    def _to_scene_act(cls, record: Action) -> ScriptRecord:
        assert isinstance(record, Action)

        if ActType.BR is record.type:
            return None
        elif ActType.NOTE is record.type:
            return ScriptRecord(RecordType.NOTE, record.subject, record.descs)
        elif ActType.MARK is record.type:
            return ScriptRecord(RecordType.SYMBOL, record.subject, record.descs)
        elif ActType.PLOT is record.type:
            return None
        elif ActType.TITLE is record.type:
            return ScriptRecord(RecordType.TITLE, record.subject, [], -1)
        elif record.type in [ActType.NONE, ActType.SAME]:
            return None
        elif ActType.TALK is record.type:
            return ScriptRecord(RecordType.DIALOGUE, record.subject, record.descs)
        elif record.type in [ActType.THINK, ActType.EXPLAIN]:
            return ScriptRecord(RecordType.MONOLOGUE, record.subject, record.descs)
        else:
            return ScriptRecord(RecordType.DESCRIPTION, record.subject, record.descs)

    @classmethod
    def _to_scene_head(cls, index: int, record: SceneInfo) -> ScriptRecord:
        assert isinstance(index, int)
        assert isinstance(record, SceneInfo)

        return ScriptRecord(RecordType.TITLE, record.title, [str(index)], record.level)

    @classmethod
    def _to_scene_spin(cls, record: SceneInfo) -> ScriptRecord:
        assert isinstance(record, SceneInfo)

        if 'nospin' in record.flags:
            return None

        return ScriptRecord(
                RecordType.SPIN, '', [],
                SpinInfo(
                    record.camera,
                    record.stage,
                    record.year,
                    record.date,
                    record.time,
                    record.clock,
                    ))

    @classmethod
    def _to_scene_control(cls, record: Instruction) -> ScriptRecord:
        assert isinstance(record, Instruction)

        if InstType.PARAGRAPH_START is record.type:
            return None
        elif InstType.PARAGRAPH_END is record.type:
            return None
        else:
            return None

    def _get_scene_end() -> ScriptRecord:
        return ScriptRecord(RecordType.SCENE_END, '', [])


class TagConverter(object):

    @classmethod
    def conv_callings_and_tags(cls, data: list, tags: dict, callings: dict) -> list:
        assert isinstance(data, list)
        assert isinstance(tags, dict)
        assert isinstance(callings, dict)

        tmp = []

        for record in data:
            assert isinstance(record, ScriptRecord)
            if RecordType.SPIN is record.type:
                tmp.append(cls._conv_spin(record, tags))
            elif record.type in NORMAL_DESCS:
                tmp.append(cls._conv_desc(record, callings))
            else:
                tmp.append(record)

        logger.debug(msg.PROC_MESSAGE.format(proc=f"tag converted scripts data: {PROC}"))

        return tmp

    def _conv_desc(record: ScriptRecord, callings: dict) -> ScriptRecord:
        assert isinstance(record, ScriptRecord)
        assert isinstance(callings, dict)

        if record.subject in callings:
            calling = callings[record.subject]
            return ScriptRecord(record.type,
                    calling['S'],
                    [translate_tags_str(d, calling) for d in record.descs],
                    record.note)
        else:
            return record

    def _conv_spin(record: ScriptRecord, tags: dict) -> ScriptRecord:
        assert isinstance(record, ScriptRecord)
        assert isinstance(tags, dict)

        info = assertion.is_instance(record.note, SpinInfo)

        return ScriptRecord(record.type, record.subject, record.descs,
                SpinInfo(
                    translate_tags_str(info.subject, tags, True, None),
                    translate_tags_str(info.stage, tags, True, None),
                    translate_tags_str(info.year, tags, True, None),
                    translate_tags_str(info.date, tags, True, None),
                    translate_tags_str(info.time, tags, True, None),
                    info.clock,
                    ))


class Formatter(object):

    @classmethod
    def format_data(cls, data: list, is_comment: bool) -> list:
        assert isinstance(data, list)
        assert isinstance(is_comment, bool)

        tmp = []

        for record in data:
            assert isinstance(record, ScriptRecord)
            if RecordType.TITLE is record.type:
                ret = cls._to_title(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br(2))
            elif RecordType.BR is record.type:
                tmp.append(get_br())
            elif RecordType.SYMBOL is record.type:
                ret = cls._to_symbol(record)
                if ret:
                    tmp.append(get_br())
                    tmp.append(ret)
                    tmp.append(get_br(2))
            elif RecordType.SPIN is record.type:
                ret = cls._to_spin(record)
                if ret:
                    tmp.append(get_br())
                    tmp.append(ret)
                    tmp.append(get_br(2))
            elif RecordType.SCENE_END is record.type:
                tmp.append(get_br())
            elif RecordType.NOTE is record.type:
                if is_comment:
                    ret = cls._to_comment(record)
                    if ret:
                        tmp.append(ret)
                        tmp.append(get_br())
            elif RecordType.DESCRIPTION is record.type:
                ret = cls._to_description(record)
                if ret:
                    tmp.append(get_indent(3))
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.DIALOGUE is record.type:
                ret = cls._to_dialogue(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.MONOLOGUE is record.type:
                ret = cls._to_dialogue(record, ('『', '』'), 'Ｍ')
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.VOICE is record.type:
                ret = cls._to_dialogue(record, ('『', '』'))
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"formatted script data: {PROC}"))

        return tmp

    def _to_comment(record: ScriptRecord) -> str:
        assert isinstance(record, ScriptRecord)

        return markdown_comment_style_of('。'.join(record.descs))

    def _to_description(record: ScriptRecord) -> str:
        assert isinstance(record, ScriptRecord)

        return join_descs(record.descs)

    def _to_dialogue(record: ScriptRecord, couple: tuple = ('「', '」'),
            suffix: str = '') -> str:
        assert isinstance(record, ScriptRecord)
        assert isinstance(couple, tuple)
        assert isinstance(suffix, str)

        start = couple[0]
        end = couple[1]

        text = join_descs(record.descs)
        _text = text.rstrip('。') if text.endswith('。') else text
        subject = f"{record.subject}{suffix}"
        if _text.startswith(start):
            return f"{subject}{_text}"
        else:
            return f"{subject}{start}{_text}{end}"

    def _to_spin(record: ScriptRecord) -> str:
        assert isinstance(record, ScriptRecord)

        info = assertion.is_instance(record.note, SpinInfo)

        return f"○{info.stage}（{info.time}）"

    def _to_symbol(record: ScriptRecord) -> str:
        assert isinstance(record, ScriptRecord)

        descs = '\n'.join(record.descs)
        return descs

    def _to_title(record: ScriptRecord) -> str:
        assert isinstance(record, ScriptRecord)

        head = '#' + '#' * int(record.note) if record.note != -1 else ''
        index = record.descs[0]
        return f"{head} {index}. {record.subject}"
