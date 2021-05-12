"""Build struct module."""

# Official Libraries
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any


# My Modules
from sms.commons.format import get_br, get_breakline, get_indent
from sms.commons.format import markdown_comment_style_of
from sms.db.outputsdata import OutputsData
from sms.db.storydata import StoryData
from sms.objs.action import Action
from sms.objs.basecode import BaseCode
from sms.objs.instruction import Instruction
from sms.objs.sceneend import SceneEnd
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.types.action import ActType, NORMAL_ACTION
from sms.utils import assertion
from sms.utils.log import logger
from sms.utils.strtranslate import translate_tags_str, translate_tags_text_list


__all__ = (
        'build_struct',
        )


# Define Constants
PROC = 'BUILD STRUCT'


class RecordType(Enum):
    NONE = auto()
    ACT = auto()
    SCENE_END = auto()
    TITLE = auto()
    SPIN = auto()


@dataclass
class SpinInfo(object):
    subject: str
    stage: str
    year: str
    date: str
    time: str
    clock: str


@dataclass
class StructRecord(object):
    type: RecordType
    act: ActType
    subject: str
    outline: str
    note: Any = None


# Main
def build_struct(story_data: StoryData, tags: dict, callings: dict,
        is_comment: bool) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(callings, dict)
    assert isinstance(is_comment, bool)

    logger.debug(msg.PROC_START.format(proc=PROC))

    structs = Converter.structs_data_from(story_data)
    if not structs:
        return None

    updated_tags = TagConverter.conv_callings_and_tags(structs, tags, callings)
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
    def structs_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []
        indices = [0]

        for record in story_data.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, SceneInfo):
                if record.level >= len(indices):
                    indices.append(0)
                indices[record.level] += 1
                tmp.append(cls._to_scene_head(indices[record.level], record))
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
                continue
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted structs data: {PROC}"))

        return tmp

    def _to_scene_act(record: Action) -> StructRecord:
        assert isinstance(record, Action)

        if record.type in NORMAL_ACTION:
            return StructRecord(RecordType.ACT, record.type,
                    record.subject, record.outline)
        else:
            return None

    def _to_scene_head(index: int, record: SceneInfo) -> StructRecord:
        assert isinstance(index, int)
        assert isinstance(record, SceneInfo)

        return StructRecord(RecordType.TITLE, ActType.TITLE,
                record.title, str(index), record.level)

    def _to_scene_spin(record: SceneInfo) -> StructRecord:
        assert isinstance(record, SceneInfo)

        if 'nospin' in record.flags:
            return None
        return StructRecord(RecordType.SPIN, ActType.NONE, '', [],
                SpinInfo(
                    record.camera,
                    record.stage,
                    record.year,
                    record.date,
                    record.time,
                    record.clock,
                    ))

    def _get_scene_end() -> StructRecord:
        return StructRecord(RecordType.SCENE_END, ActType.NONE, '', '')


class TagConverter(object):

    @classmethod
    def conv_callings_and_tags(cls, data: list, tags: dict, callings: dict) -> list:
        assert isinstance(data, list)
        assert isinstance(tags, dict)
        assert isinstance(callings, dict)

        tmp = []

        for record in data:
            assert isinstance(record, StructRecord)
            if RecordType.SPIN is record.type:
                tmp.append(cls._conv_spin(record, tags))
            elif record.type in [RecordType.ACT]:
                tmp.append(cls._conv_act(record, callings))
            else:
                tmp.append(record)

        logger.debug(msg.PROC_MESSAGE.format(proc=f"tag converted structs data: {PROC}"))

        return tmp

    def _conv_act(record: StructRecord, callings: dict) -> StructRecord:
        assert isinstance(record, StructRecord)
        assert isinstance(callings, dict)

        if record.subject in callings:
            calling = callings[record.subject]
            return StructRecord(record.type, record.act,
                    calling['S'],
                    translate_tags_str(record.outline, calling),
                    record.note)
        else:
            return record

    def _conv_spin(record: StructRecord, tags: dict) -> StructRecord:
        assert isinstance(record, StructRecord)
        assert isinstance(tags, dict)

        info = assertion.is_instance(record.note, SpinInfo)

        return StructRecord(record.type, record.act, record.subject, record.outline,
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
            assert isinstance(record, StructRecord)
            if RecordType.TITLE is record.type:
                ret = cls._to_title(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br(2))
            elif RecordType.SCENE_END is record.type:
                tmp.append(get_br(2))
            elif RecordType.SPIN is record.type:
                tmp.append(cls._to_spin(record))
                tmp.append(get_br())
            elif RecordType.ACT is record.type:
                ret = cls._to_act(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"formatted structs data: {PROC}"))

        return tmp

    def _to_act(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        subject = record.subject if record.subject else '――'
        outline = record.outline if record.outline else '――'
        indent = get_indent(2)

        if ActType.BE is record.act:
            return f"{indent}[{subject}]（いる）{outline}"
        elif ActType.COME is record.act:
            return f"{indent}[{subject}]（来る）{outline}"
        elif ActType.DO is record.act:
            return f"{indent}[{subject}]（行動）{outline}"
        elif ActType.DRAW is record.act:
            return f"{indent}（描画）[{subject}]{outline}"
        elif ActType.EXPLAIN is record.act:
            return f"{indent}（説明）[{subject}]{outline}"
        elif ActType.FACE is record.act:
            return f"{indent}[{subject}]（表情）{outline}"
        elif ActType.FEEL is record.act:
            return f"{indent}[{subject}]（感情）{outline}"
        elif ActType.GO is record.act:
            return f"{indent}[{subject}]（去る）{outline}"
        elif ActType.TALK is record.act:
            return f"{subject}「{outline}」"
        elif ActType.THINK is record.act:
            return f"{subject}『{outline}』"
        elif ActType.VOICE is record.act:
            return f"{subject}（声）『{outline}』"
        elif ActType.WEAR is record.act:
            return f"{indent}[{subject}]（服装）{outline}"
        else:
            return None

    def _to_comment(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        return markdown_comment_style_of(record.subject)

    def _to_spin(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        info = assertion.is_instance(record.note, SpinInfo)

        camera = info.subject
        stage = info.stage
        year = info.year
        date = info.date
        time = info.time
        clock = info.clock

        return f"○{stage}（{time}/{clock}） - {date}/{year} - [{camera}]"

    def _to_title(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        head = '#' + '#' * int(record.note) if record.note != -1 else ''
        index = record.outline
        return f"{head} {index}. {record.subject}"
