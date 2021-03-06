"""Scene info build module."""

# Official Libraries
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any


# My Modules
from sms.commons.format import get_br, get_breakline
from sms.db.outputsdata import OutputsData
from sms.db.storydata import StoryData
from sms.objs.action import Action
from sms.objs.basecode import BaseCode
from sms.objs.sceneend import SceneEnd
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.types.action import ActType
from sms.utils import assertion
from sms.utils.log import logger
from sms.utils.strings import just_string_of
from sms.utils.strtranslate import translate_tags_str, translate_tags_text_list


__all__ = (
        'build_info',
        )


# Define Constants
PROC = 'BUILD INFO'


class RecordType(Enum):
    NONE = auto()
    DATA_HEAD = auto()
    TITLE = auto()
    TRANSITION = auto()
    PERSON_INFO = auto()
    ITEM_INFO = auto()
    FLAG_INFO = auto()


@dataclass
class InfoRecord(object):
    type: RecordType
    level: int
    index: int
    subject: str
    outline: str
    note: Any = None


@dataclass
class TransitionInfo(object):
    title: str
    camera: str
    stage: str
    location: str
    year: str
    date: str
    time: str
    clock: str


class PersonInOut(Enum):
    BE = auto()
    IN = auto()
    OUT = auto()
    WEAR = auto()


@dataclass
class PersonInfo(object):
    type: PersonInOut


@dataclass
class ItemInfo(object):
    have: str


@dataclass
class FlagInfo(object):
    foreshadow: str
    payoff: str


# Main
def build_info(story_data: StoryData, tags: dict, callings: dict) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(callings, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    infos = Converter.infos_data_from(story_data)
    if not infos:
        return None

    updated_tags = TagConverter.conv_callings_and_tags(infos, tags, callings)
    if not updated_tags:
        return None

    formatted = Formatter.format_data(updated_tags)
    if not formatted:
        return None

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return OutputsData(translated)


# Processes
class Converter(object):

    @classmethod
    def infos_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []

        transitions = TransitionInfoConv.transitions_data_from(story_data)
        if not transitions:
            return None

        persons = PersonInfoConv.personinfos_data_from(story_data)
        if not persons:
            return None

        items = ItemInfoConv.iteminfos_data_from(story_data)
        if not items:
            return None

        flags = FlagInfoConv.flags_data_from(story_data)
        if not flags:
            return None

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted infos data: {PROC}"))

        tmp = transitions + persons + items + flags

        return tmp


class TagConverter(object):

    @classmethod
    def conv_callings_and_tags(cls, data: list, tags: dict, callings: dict) -> list:
        assert isinstance(data, list)
        assert isinstance(tags, dict)
        assert isinstance(callings, dict)

        tmp = []

        for record in data:
            assert isinstance(record, InfoRecord)
            if RecordType.TRANSITION is record.type:
                tmp.append(cls._conv_transition(record, tags))
            elif RecordType.PERSON_INFO is record.type:
                tmp.append(cls._conv_person(record, callings, tags))
            elif RecordType.ITEM_INFO is record.type:
                tmp.append(cls._conv_item(record, callings, tags))
            elif RecordType.FLAG_INFO is record.type:
                tmp.append(cls._conv_flag(record, callings, tags))
            else:
                tmp.append(record)

        logger.debug(msg.PROC_MESSAGE.format(proc=f"tag converted infos data: {PROC}"))

        return tmp

    def _conv_flag(record: InfoRecord, callings: dict, tags: dict) -> InfoRecord:
        assert isinstance(record, InfoRecord)
        assert isinstance(callings, dict)
        assert isinstance(tags, dict)

        info = assertion.is_instance(record.note, FlagInfo)
        subject = record.subject
        outline = record.outline
        foreshadow = info.foreshadow
        payoff = info.payoff

        if subject in callings:
            calling = callings[record.subject]
            subject = calling['S']
            outline = translate_tags_str(outline, calling)
            foreshadow = translate_tags_str(foreshadow, calling)
            payoff = translate_tags_str(payoff, calling)
        return InfoRecord(record.type, record.level, record.index,
                translate_tags_str(subject, tags),
                translate_tags_str(outline, tags),
                FlagInfo(
                    translate_tags_str(foreshadow, tags),
                    translate_tags_str(payoff, tags)
                ))

    def _conv_item(record: InfoRecord, callings: dict, tags: dict) -> InfoRecord:
        assert isinstance(record, InfoRecord)
        assert isinstance(callings, dict)
        assert isinstance(tags, dict)

        info = assertion.is_instance(record.note, ItemInfo)
        subject = record.subject
        outline = record.outline
        have = info.have

        if record.subject in callings:
            calling = callings[record.subject]
            outline = translate_tags_str(outline, calling)
            have = translate_tags_str(have, calling)
        return InfoRecord(record.type, record.level, record.index,
                translate_tags_str(subject, tags),
                translate_tags_str(outline, tags),
                ItemInfo(
                    translate_tags_str(have, tags),
                    ))

    def _conv_person(record: InfoRecord, callings: dict, tags: dict) -> InfoRecord:
        assert isinstance(record, InfoRecord)
        assert isinstance(callings, dict)
        assert isinstance(tags, dict)

        info = assertion.is_instance(record.note, PersonInfo)
        subject = record.subject
        outline = record.outline

        if record.subject in callings:
            calling = callings[record.subject]
            outline = translate_tags_str(outline, calling)
        return InfoRecord(record.type, record.level, record.index,
                translate_tags_str(subject, tags, True, None),
                translate_tags_str(outline, tags),
                info)

    def _conv_transition(record: InfoRecord, tags: dict) -> InfoRecord:
        assert isinstance(record, InfoRecord)
        assert isinstance(tags, dict)

        info = assertion.is_instance(record.note, TransitionInfo)

        return InfoRecord(record.type, record.level, record.index,
                record.subject, record.outline,
                TransitionInfo(
                    translate_tags_str(info.title, tags),
                    translate_tags_str(info.camera, tags, True, None),
                    translate_tags_str(info.stage, tags, True, None),
                    info.location,
                    translate_tags_str(info.year, tags),
                    translate_tags_str(info.date, tags),
                    translate_tags_str(info.time, tags, True, None),
                    info.clock,
                    ))


class TransitionInfoConv(object):

    @classmethod
    def transitions_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []
        indices = [0]

        tmp.append(InfoRecord(RecordType.DATA_HEAD, 0, 0, 'TRANSITION INFO', ''))

        for record in story_data.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, SceneInfo):
                if record.level >= len(indices):
                    indices.append(0)
                indices[record.level] += 1
                if 'nospin' in record.flags:
                    continue
                ret = cls._to_transition_info(indices[record.level], record)
                if ret:
                    tmp.append(ret)
            elif isinstance(record, SceneEnd):
                pass
            elif isinstance(record, Action):
                continue
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted transitions data: {PROC}"))

        return tmp

    def _to_transition_info(index: int, record: SceneInfo) -> InfoRecord:
        assert isinstance(index, int)
        assert isinstance(record, SceneInfo)

        return InfoRecord(RecordType.TRANSITION, record.level, index, '', '',
                TransitionInfo(
                    record.title,
                    record.camera,
                    record.stage,
                    record.location,
                    record.year,
                    record.date,
                    record.time,
                    record.clock,
                    ))


class PersonInfoConv(object):

    @classmethod
    def personinfos_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []
        indices = [0]
        cur_level = 0
        cur_index = 0

        tmp.append(InfoRecord(RecordType.DATA_HEAD, 0, 0, 'PERSON INFO', ''))

        for record in story_data.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, SceneInfo):
                if record.level >= len(indices):
                    indices.append(0)
                cur_level = record.level
                indices[record.level] += 1
                cur_index = indices[record.level]
            elif isinstance(record, SceneEnd):
                continue
            elif isinstance(record, Action):
                ret = cls._to_person_info(cur_level, cur_index, record)
                if ret:
                    tmp.append(ret)
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted person infos data: {PROC}"))

        return tmp

    def _to_person_info(level: int, index: int, record: Action) -> InfoRecord:
        assert isinstance(level, int)
        assert isinstance(index, int)
        assert isinstance(record, Action)

        into = outto = wear = ''
        type = PersonInOut.BE

        if ActType.BE is record.type:
            type = PersonInOut.BE
        elif ActType.COME is record.type:
            type = PersonInOut.IN
        elif ActType.GO is record.type:
            type = PersonInOut.OUT
        elif ActType.WEAR is record.type:
            type = PersonInOut.WEAR
        else:
            return None

        return InfoRecord(RecordType.PERSON_INFO, level, index,
                record.subject, record.outline,
                PersonInfo(type))


class ItemInfoConv(object):

    @classmethod
    def iteminfos_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []
        indices = [0]
        cur_level = 0
        cur_index = 0
        tmp.append(InfoRecord(RecordType.DATA_HEAD, 0, 0, 'ITEM INFO', ''))

        for record in story_data.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, SceneInfo):
                if record.level >= len(indices):
                    indices.append(0)
                cur_level = record.level
                indices[record.level] += 1
                cur_index = indices[record.level]
            elif isinstance(record, SceneEnd):
                continue
            elif isinstance(record, Action):
                ret = cls._to_item_info(cur_level, cur_index, record)
                if ret:
                    tmp.append(ret)
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted item infos data: {PROC}"))

        return tmp

    def _to_item_info(level: int, index: int, record: Action) -> InfoRecord:
        assert isinstance(record, Action)

        if ActType.HAVE is record.type:
            return InfoRecord(RecordType.ITEM_INFO, level, index,
                record.subject, record.outline,
                ItemInfo(record.outline))
        else:
            return None


class FlagInfoConv(object):

    @classmethod
    def flags_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []
        indices = [0]
        cur_level = 0
        cur_index = 0
        tmp.append(InfoRecord(RecordType.DATA_HEAD, 0, 0, 'FLAG INFO', ''))

        for record in story_data.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, SceneInfo):
                if record.level <= len(indices):
                    indices.append(0)
                cur_level = record.level
                indices[record.level] += 1
                cur_index = indices[record.level]
            elif isinstance(record, SceneEnd):
                continue
            elif isinstance(record, Action):
                ret = cls._to_flag_info(cur_level, cur_index, record)
                if ret:
                    tmp.append(ret)
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted flags data: {PROC}"))

        return tmp

    def _to_flag_info(level: int, index: int, record: Action) -> InfoRecord:
        assert isinstance(level, int)
        assert isinstance(index, int)
        assert isinstance(record, Action)

        foreshadow = payoff = ''

        if ActType.FORESHADOW is record.type:
            foreshadow = record.outline
        elif ActType.PAYOFF is record.type:
            payoff = record.outline
        else:
            return None

        return InfoRecord(RecordType.FLAG_INFO, level, index,
                record.subject, record.outline,
                FlagInfo(foreshadow, payoff))


class Formatter(object):

    @classmethod
    def format_data(cls, data: list) -> list:
        assert isinstance(data, list)

        tmp = []
        tmp.append('SCENE INFO DATA\n===\n\n')

        for record in data:
            assert isinstance(record, InfoRecord)
            if RecordType.DATA_HEAD is record.type:
                tmp.append(get_breakline())
                tmp.append(cls._to_data_head(record))
                tmp.append(get_br(2))
            elif RecordType.TITLE is record.type:
                pass
            elif RecordType.TRANSITION is record.type:
                ret = cls._to_transision(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.PERSON_INFO is record.type:
                ret = cls._to_person(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.ITEM_INFO is record.type:
                ret = cls._to_item(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.FLAG_INFO is record.type:
                ret = cls._to_flag(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"formatted infos data: {PROC}"))

        return tmp

    def _to_data_head(record: InfoRecord) -> str:
        assert isinstance(record, InfoRecord)

        return f"## {record.subject}"

    @classmethod
    def _to_flag(cls, record: InfoRecord) -> str:
        assert isinstance(record, InfoRecord)

        info = assertion.is_instance(record.note, FlagInfo)

        level = str(record.level)
        index = str(record.index)
        subject = record.subject
        foreshadow = info.foreshadow
        payoff = info.payoff

        return cls._conv_flag(level, index, subject, foreshadow, payoff)

    @classmethod
    def _to_item(cls, record: InfoRecord) -> str:
        assert isinstance(record, InfoRecord)

        info = assertion.is_instance(record.note, ItemInfo)
        level = str(record.level)
        index = str(record.index)
        subject = record.subject
        have = info.have

        return cls._conv_item(level, index, subject, have)

    @classmethod
    def _to_person(cls, record: InfoRecord) -> str:
        assert isinstance(record, InfoRecord)

        info = assertion.is_instance(record.note, PersonInfo)

        level = str(record.level)
        index = str(record.index)
        subject = record.subject
        outline = record.outline

        return cls._conv_person(level, index, subject, info.type, outline)

    @classmethod
    def _to_transision(cls, record: InfoRecord) -> str:
        assert isinstance(record, InfoRecord)

        info = assertion.is_instance(record.note, TransitionInfo)

        level = str(record.level)
        index = str(record.index)
        title = info.title
        stage = info.stage
        time = info.time
        clock = info.clock
        date = info.date
        year = info.year
        camera = info.camera

        return cls._conv_transition(level, index, title, stage, time, clock, date, year, camera)

    @classmethod
    def _to_transision_breakline(cls) -> str:
        level = index = stage = time = clock = date = year = camera = '----'
        return cls._conv_transition(level, index, stage, time, clock, date, year, camera)

    def _conv_flag(level: str, index: str, subject: str,
            foreshadow: str, payoff: str) -> str:
        assert isinstance(level, str)
        assert isinstance(index, str)
        assert isinstance(subject, str)
        assert isinstance(foreshadow, str)
        assert isinstance(payoff, str)

        _level = just_string_of(level, 4)
        _index = just_string_of(index, 4)
        _subject = just_string_of(subject, 16)
        _foreshadow = just_string_of(foreshadow, 24)
        _payoff = just_string_of(payoff, 24)

        return f"| {_level} | {_index} | {_subject} | {_foreshadow} | {_payoff} |"

    def _conv_item(level: str, index: str, subject: str, have: str) -> str:
        assert isinstance(level, str)
        assert isinstance(index, str)
        assert isinstance(subject, str)
        assert isinstance(have, str)

        _level = just_string_of(level, 4)
        _index = just_string_of(index, 4)
        _subject = just_string_of(subject, 16)
        _have = just_string_of(have, 16)

        return f"| {_level} | {_index} | {_subject} | {_have} |"

    def _conv_person(level: str, index: str, subject: str, type: PersonInOut,
            outline: str) -> str:
        assert isinstance(level, str)
        assert isinstance(index, str)
        assert isinstance(subject, str)
        assert isinstance(type, PersonInOut)
        assert isinstance(outline, str)

        be = into = outto = wear = ''

        if PersonInOut.BE is type:
            be = 'BE'
        elif PersonInOut.IN is type:
            into = 'IN'
        elif PersonInOut.OUT is type:
            outto = 'OUT'
        elif PersonInOut.WEAR is type:
            wear = 'WEAR'
        else:
            logger.warning(
                    msg.ERR_FAIL_UNKNOWN_DATA_WITH_DATA.format(data=f"format person info: {PROC}"),
                    type)

        _level = just_string_of(level, 4)
        _index = just_string_of(index, 4)
        _subject = just_string_of(subject, 16)
        _be = just_string_of(be, 4)
        _in = just_string_of(into, 4)
        _out = just_string_of(outto, 4)
        _wear = just_string_of(wear, 4)
        _outline = just_string_of(outline, 16)

        return f"| {_level} | {_index} | {_subject} | {_be} | {_in} | {_out} | {_wear} | {_outline} |"

    def _conv_transition(level: str, index: str, title: str, stage: str,
            time: str, clock: str, date: str, year: str, camera: str) -> str:
        assert isinstance(level, str)
        assert isinstance(index, str)
        assert isinstance(title, str)
        assert isinstance(stage, str)
        assert isinstance(time, str)
        assert isinstance(clock, str)
        assert isinstance(date, str)
        assert isinstance(year, str)
        assert isinstance(camera, str)

        _level = just_string_of(level, 4)
        _index = just_string_of(index, 4)
        _title = just_string_of(title, 16)
        _stage = just_string_of(stage, 16)
        _time = just_string_of(time, 6)
        _date = just_string_of(date, 6)
        _year = just_string_of(year, 6)
        _camera = just_string_of(camera, 16)
        _clock = just_string_of(clock, 6)

        return f"| {_level} | {_index} | {_title} | {_stage} | {_time} | {_clock} | {_date} | {_year} | {_camera} |"
