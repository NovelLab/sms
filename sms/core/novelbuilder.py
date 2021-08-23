"""Build novel module."""

# Official Libraries
from enum import auto, Enum
from dataclasses import dataclass, field
from typing import Any
import re

# My Modules
from sms.commons.format import get_br, get_indent
from sms.commons.format import join_descs
from sms.commons.format import markdown_comment_style_of
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
from sms.utils.dicts import dict_sorted
from sms.utils.log import logger
from sms.utils.strtranslate import translate_tags_str
from sms.utils.strtranslate import translate_tags_text_list


__all__ = (
        'build_novel',
        )

# Define Constants
PROC = 'BUILD NOVEL'


class RecordType(Enum):
    NONE = auto()
    DESCRIPTION = auto()
    DIALOGUE = auto()
    VOICE = auto()
    TITLE = auto()
    # symbol
    BR = auto()
    SYMBOL = auto()
    PLAIN = auto()
    # data
    SCENE_END = auto()
    PR_START = auto()
    PR_END = auto()
    # others
    NOTE = auto()


NORMAL_DESCS = [
        RecordType.DESCRIPTION,
        RecordType.DIALOGUE,
        RecordType.VOICE,
        ]


@dataclass
class NovelRecord(object):
    type: RecordType
    subject: str
    descs: list = field(default_factory=list)
    note: Any = None


# Main
def build_novel(story_data: StoryData, tags: dict, callings: dict,
        is_comment: bool) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(callings, dict)
    assert isinstance(is_comment, bool)

    logger.debug(msg.PROC_START.format(proc=PROC))

    novels = Converter.novels_data_from(story_data)
    if not novels:
        return None

    updated_tags = TagConverter.conv_callings_and_tags(novels, tags, callings)
    if not updated_tags:
        return None

    formatted = Formatter.format_data(updated_tags, is_comment)
    if not formatted:
        return None

    translated = translate_tags_text_list(formatted, dict_sorted(tags, True))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return OutputsData(translated)


# Processes
class Converter(object):

    @classmethod
    def novels_data_from(cls, story_data: StoryData) -> list:
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

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted novels data: {PROC}"))

        return tmp

    @classmethod
    def _to_scene_act(cls, record: Action) -> NovelRecord:
        assert isinstance(record, Action)

        if ActType.BR is record.type:
            return NovelRecord(RecordType.BR, '', [])
        elif ActType.MARK is record.type:
            return NovelRecord(RecordType.SYMBOL, record.subject, [record.outline])
        elif not record.descs:
            return None
        elif ActType.NOTE is record.type:
            return NovelRecord(RecordType.NOTE, record.subject, record.descs)
        elif ActType.PLOT is record.type:
            return None
        elif ActType.TITLE is record.type:
            return NovelRecord(RecordType.TITLE, record.subject, [], -1)
        elif record.type in [ActType.NONE, ActType.SAME]:
            return None
        elif ActType.TALK is record.type:
            return NovelRecord(RecordType.DIALOGUE, record.subject, record.descs)
        elif ActType.VOICE is record.type:
            return NovelRecord(RecordType.VOICE, record.subject, record.descs)
        elif ActType.PLAIN is record.type:
            return NovelRecord(RecordType.PLAIN, record.subject, record.descs)
        else:
            return NovelRecord(RecordType.DESCRIPTION, record.subject, record.descs)

    @classmethod
    def _to_scene_head(cls, index: int, record: SceneInfo) -> NovelRecord:
        assert isinstance(index, int)
        assert isinstance(record, SceneInfo)

        return NovelRecord(RecordType.TITLE, record.title, [str(index)], record.level)

    @classmethod
    def _to_scene_control(cls, record: Instruction) -> NovelRecord:
        assert isinstance(record, Instruction)

        if InstType.PARAGRAPH_START is record.type:
            return NovelRecord(RecordType.PR_START, '', [])
        elif InstType.PARAGRAPH_END is record.type:
            return NovelRecord(RecordType.PR_END, '', [])
        else:
            return None

    def _get_scene_end() -> NovelRecord:
        return NovelRecord(RecordType.SCENE_END, '', [])


class TagConverter(object):

    @classmethod
    def conv_callings_and_tags(cls, data: list, tags: dict, callings: dict) -> list:
        assert isinstance(data, list)
        assert isinstance(tags, dict)
        assert isinstance(callings, dict)

        tmp = []

        for record in data:
            assert isinstance(record, NovelRecord)
            if record.type in NORMAL_DESCS:
                tmp.append(cls._conv_desc(record, callings))
            else:
                tmp.append(record)

        logger.debug(msg.PROC_MESSAGE.format(proc=f"tag converted novels data: {PROC}"))

        return tmp

    def _conv_desc(record: NovelRecord, callings: dict) -> NovelRecord:
        assert isinstance(record, NovelRecord)
        assert isinstance(callings, dict)

        if record.subject in callings:
            calling = dict_sorted(callings[record.subject], True)
            return NovelRecord(record.type,
                    calling['S'],
                    [translate_tags_str(d, calling) for d in record.descs],
                    record.note)
        else:
            return record


class Formatter(object):

    @classmethod
    def format_data(cls, data: list, is_comment: bool) -> list:
        assert isinstance(data, list)
        assert isinstance(is_comment, bool)

        tmp = []
        is_nobr = False
        is_firstindent = False

        for record in data:
            assert isinstance(record, NovelRecord)
            if RecordType.TITLE is record.type:
                ret = cls._to_title(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br(2))
            elif RecordType.BR is record.type:
                tmp.append(get_br())
            elif RecordType.PR_START is record.type:
                is_nobr = True
                is_firstindent = False
            elif RecordType.PR_END is record.type:
                is_nobr = False
                tmp.append(get_br())
            elif RecordType.SYMBOL is record.type:
                tmp.append(get_br())
                tmp.append(cls._to_symbol(record))
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
                    if is_nobr:
                        if not is_firstindent:
                            tmp.append(get_indent(1))
                            is_firstindent = True
                        tmp.append(ret)
                    else:
                        tmp.append(get_indent(1))
                        tmp.append(ret)
                        tmp.append(get_br())
            elif RecordType.DIALOGUE is record.type:
                ret = cls._to_dialogue(record)
                if ret:
                    if is_nobr:
                        if not is_firstindent:
                            is_firstindent = True
                        tmp.append(ret)
                    else:
                        tmp.append(ret)
                        tmp.append(get_br())
            elif RecordType.VOICE is record.type:
                ret = cls._to_dialogue(record, ('『', '』'))
                if ret:
                    if is_nobr:
                        if not is_firstindent:
                            is_firstindent = True
                        tmp.append(ret)
                    else:
                        tmp.append(ret)
                        tmp.append(get_br())
            elif RecordType.PLAIN is record.type:
                ret = cls._to_plain(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"formatted novels data: {PROC}"))

        return tmp

    def _to_comment(record: NovelRecord) -> str:
        assert isinstance(record, NovelRecord)

        return markdown_comment_style_of('。'.join(record.descs))

    def _to_description(record: NovelRecord) -> str:
        assert isinstance(record, NovelRecord)

        return join_descs(_conv_dialogue_mark(record.descs))

    def _to_plain(record: NovelRecord) -> str:
        assert isinstance(record, NovelRecord)

        return "".join(record.descs)

    def _to_dialogue(record: NovelRecord, couple: tuple = ('「', '」')) -> str:
        assert isinstance(record, NovelRecord)
        assert isinstance(couple, tuple)

        start = couple[0]
        end = couple[1]

        text = join_descs(_conv_dialogue_mark_in_dialogues(record.descs))
        _text = text.rstrip('。') if text.endswith('。') else text
        if _text.startswith(start) and not _text.endswith(end):
            return _text if _text.endswith(('、', '。', '！', '？', '!', '?')) else f"{_text}。"
        elif not _text.startswith(start):
            return f"{start}{_text}{end}"
        else:
            return _text

    def _to_symbol(record: NovelRecord) -> str:
        assert isinstance(record, NovelRecord)

        descs = '\n'.join(record.descs)
        return descs

    def _to_title(record: NovelRecord) -> str:
        assert isinstance(record, NovelRecord)

        head = '#' + '#' * int(record.note) if record.note != -1 else ''
        index = record.descs[0]
        return f"{head} {index}. {record.subject}"


# Private Functions
def _conv_dialogue_mark(data: list) -> list:
    assert isinstance(data, list)

    tmp = []

    for line in data:
        assert isinstance(line, str)
        if line.startswith(':'):
            tmp.append(f"「{line[1:]}」")
        else:
            tmp.append(line)
    return tmp


def _conv_dialogue_mark_in_dialogues(data: list) -> list:
    assert isinstance(data, list)

    tmp = []

    for line in data:
        assert isinstance(line, str)
        if ':' in line:
            if line.startswith(':'):
                tmp.append(f"「{line[1:]}」")
            elif re.search(r'^[a-zA-Z0-9]*:', line):
                part = re.search(r'^[a-zA-Z0-9]*:', line).group()
                tmp.append(f"「{line.replace(part, '')}」")
        else:
            tmp.append(line)
    return tmp
