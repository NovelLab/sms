"""Build struct module."""

# Official Libraries
import copy
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any


# My Modules
from sms.commons.format import get_br, get_indent
from sms.commons.format import markdown_comment_style_of
from sms.db.outputsdata import OutputsData
from sms.db.storydata import StoryData
from sms.objs.action import Action
from sms.objs.basecode import BaseCode
from sms.objs.instruction import Instruction
from sms.objs.sceneend import SceneEnd
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.types.action import ActType, NORMAL_ACTS, OBJECT_ACTS
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
    OBJECT = auto()
    OBJECT_PACK = auto()
    PERSON = auto()
    PERSON_PACK = auto()
    SKY = auto()
    LIGHT = auto()
    SYMBOL = auto()
    FLAG = auto()
    TIME = auto()


DIALOGUE_ACTS = [
        ActType.TALK,
        ActType.VOICE,
        ]

DOING_ACTS = [
        ActType.BE,
        ActType.COME,
        ActType.DO,
        ActType.GO,
        ]

DRAW_ACTS = [
        ActType.DISCARD,
        ActType.DRAW,
        ActType.FACE,
        ActType.HAVE,
        ActType.LIGHT,
        ActType.PUT,
        ActType.RID,
        ActType.SKY,
        ActType.WEAR,
        ]

FLAG_ACTS = [
        ActType.FORESHADOW,
        ActType.PAYOFF,
        ]

SELECT_ACTS = [
        ActType.CHOICE,
        ActType.SELECTION,
        ]

STATE_ACTS = [
        ActType.KNOW,
        ActType.PROMISE,
        ActType.REMEMBER,
        ActType.STATE,
        ActType.WHY,
        ]

TIME_ACTS = [
        ActType.ELAPSE,
        ]

THINKING_ACTS = [
        ActType.EXPLAIN,
        ActType.FEEL,
        ActType.THINK,
        ]


@dataclass
class SpinInfo(object):
    subject: str
    stage: str
    location: str
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

    structs = Converter.structs_data_from(story_data, _get_person_tags(callings))
    if not structs:
        return None

    updated_tags = TagConverter.conv_callings_and_tags(structs, tags, callings)
    if not updated_tags:
        return None

    reordered = Reorder.reorder_data_from(updated_tags)
    if not reordered:
        return None

    formatted = Formatter.format_data(reordered, is_comment)
    if not formatted:
        return None

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return OutputsData(translated)


# Processes
class Converter(object):

    @classmethod
    def structs_data_from(cls, story_data: StoryData, person_tags: list) -> list:
        assert isinstance(story_data, StoryData)
        assert isinstance(person_tags, list)

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
                    if RecordType.ACT is ret.type:
                        if ret.subject in person_tags:
                            pret = cls._to_scene_person(record)
                            if pret:
                                tmp.append(pret)
            elif isinstance(record, Instruction):
                continue
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted structs data: {PROC}"))

        return tmp

    def _to_scene_act(record: Action) -> StructRecord:
        assert isinstance(record, Action)

        if record.type in NORMAL_ACTS:
            return StructRecord(RecordType.ACT, record.type,
                    record.subject, record.outline)
        elif record.type in OBJECT_ACTS:
            return StructRecord(RecordType.OBJECT, record.type,
                    record.subject, record.outline)
        elif ActType.SKY is record.type:
            return StructRecord(RecordType.SKY, record.type,
                    record.subject, record.outline)
        elif ActType.LIGHT is record.type:
            return StructRecord(RecordType.LIGHT, record.type,
                    record.subject, record.outline)
        elif ActType.MARK is record.type:
            return StructRecord(RecordType.SYMBOL, record.type,
                    record.subject, record.outline)
        elif record.type in FLAG_ACTS:
            return StructRecord(RecordType.FLAG, record.type,
                    record.subject, record.outline)
        elif record.type in TIME_ACTS:
            return StructRecord(RecordType.TIME, record.type,
                    record.subject, record.outline)
        else:
            return None

    def _to_scene_head(index: int, record: SceneInfo) -> StructRecord:
        assert isinstance(index, int)
        assert isinstance(record, SceneInfo)

        return StructRecord(RecordType.TITLE, ActType.TITLE,
                record.title, str(index), record.level)

    def _to_scene_person(record: Action) -> StructRecord:
        assert isinstance(record, Action)

        if record.subject:
            return StructRecord(RecordType.PERSON, record.type,
                    record.subject, '')
        else:
            return None

    def _to_scene_spin(record: SceneInfo) -> StructRecord:
        assert isinstance(record, SceneInfo)

        if 'nospin' in record.flags:
            return None
        return StructRecord(RecordType.SPIN, ActType.NONE, '', [],
                SpinInfo(
                    record.camera,
                    record.stage,
                    record.location,
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
            elif record.type in [RecordType.ACT, RecordType.OBJECT, RecordType.PERSON]:
                tmp.append(cls._conv_act(record, tags, callings))
            else:
                tmp.append(record)

        logger.debug(msg.PROC_MESSAGE.format(proc=f"tag converted structs data: {PROC}"))

        return tmp

    def _conv_act(record: StructRecord, tags: dict, callings: dict) -> StructRecord:
        assert isinstance(record, StructRecord)
        assert isinstance(tags, dict)
        assert isinstance(callings, dict)

        if record.subject in callings:
            calling = callings[record.subject]
            return StructRecord(record.type, record.act,
                    calling['S'],
                    translate_tags_str(record.outline, calling),
                    record.note)
        elif record.subject in tags:
            return StructRecord(record.type, record.act,
                    translate_tags_str(record.subject, tags, True, None),
                    record.outline,
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
                    info.location,
                    translate_tags_str(info.year, tags, True, None),
                    translate_tags_str(info.date, tags, True, None),
                    translate_tags_str(info.time, tags, True, None),
                    info.clock,
                    ))


class Reorder(object):

    @classmethod
    def reorder_data_from(cls, data: list) -> list:
        assert isinstance(data, list)

        tmp = []
        cache = []
        persons = []
        objects = []
        is_lighting = False
        is_int = False
        is_start_spin = False

        for record in data:
            assert isinstance(record, StructRecord)
            if RecordType.TITLE is record.type:
                tmp.append(record)
            elif RecordType.SPIN is record.type:
                tmp.append(record)
                info = assertion.is_instance(record.note, SpinInfo)
                is_int = info.location == 'INT'
                is_start_spin = True
            elif RecordType.SCENE_END is record.type:
                if not is_start_spin:
                    continue
                oret = cls._conv_object_pack(objects)
                if oret:
                    tmp.append(oret)
                pret = cls._conv_person_pack(persons)
                if pret:
                    tmp.append(pret)
                if not is_lighting:
                    tmp.append(cls._get_default_light(is_int))
                tmp.extend(copy.deepcopy(cache))
                tmp.append(record)
                # reset
                objects = []
                persons = []
                cache = []
                is_lighting = False
                is_int = False
                is_start_spin = False
            elif RecordType.OBJECT is record.type:
                objects.append(record)
            elif RecordType.PERSON is record.type:
                persons.append(record)
            elif RecordType.LIGHT is record.type:
                is_lighting = True
                cache.append(record)
            else:
                cache.append(record)

        logger.debug(msg.PROC_MESSAGE.format(proc=f"reorder struct data: {PROC}"))

        return tmp

    def _conv_object_pack(objects: list) -> StructRecord:
        assert isinstance(objects, list)

        tmp = []

        for record in objects:
            assert isinstance(record, StructRecord)
            if ActType.PUT is record.act:
                tmp.append(record.subject)
            else:
                tmp.append(f"〜{record.subject}")

        subjects = list(set(tmp))

        if subjects:
            return StructRecord(RecordType.OBJECT_PACK, ActType.NONE,
                    "/".join(subjects), "")
        else:
            return None

    def _conv_person_pack(persons: list) -> StructRecord:
        assert isinstance(persons, list)

        tmp = []

        for record in persons:
            assert isinstance(record, StructRecord)
            tmp.append(record.subject)

        subjects = list(set(tmp))

        if subjects:
            return StructRecord(RecordType.PERSON_PACK, ActType.NONE,
                    "/".join(subjects), "")
        else:
            return None

    def _get_default_light(is_int: bool) -> StructRecord:
        assert isinstance(is_int, bool)

        lux = '6' if is_int else '4'

        return StructRecord(RecordType.LIGHT, ActType.NONE, '', lux)


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
            elif RecordType.FLAG is record.type:
                ret = cls._to_flag(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.TIME is record.type:
                ret = cls._to_time(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.SYMBOL is record.type:
                ret = cls._to_symbol(record)
                if ret:
                    tmp.append(get_br())
                    tmp.append(ret)
                    tmp.append(get_br(2))
            elif RecordType.SKY is record.type:
                ret = cls._to_sky(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.LIGHT is record.type:
                ret = cls._to_light(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.OBJECT_PACK is record.type:
                ret = cls._to_object(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            elif RecordType.PERSON_PACK is record.type:
                ret = cls._to_person(record)
                if ret:
                    tmp.append(ret)
                    tmp.append(get_br())
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"formatted structs data: {PROC}"))

        return tmp

    def _to_act(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        act = assertion.is_instance(record.act, ActType)
        subject = record.subject if record.subject else '――'
        category = act.to_category()
        outline = record.outline if record.outline else '――'
        indent = get_indent(2)

        if act in DIALOGUE_ACTS:
            _outline = f"「{outline}」"
            if ActType.VOICE is act:
                _outline = f"（{category}）『{outline}』"
            return f"{subject}{_outline}"
        elif act in DOING_ACTS:
            return f"{indent}[{subject}]（{category}）{outline}"
        elif act in DRAW_ACTS:
            return f"{indent}＠（{category}）[{subject}]{outline}"
        elif act in FLAG_ACTS:
            return f"{indent}！（{category}）[{subject}]{outline}"
        elif act in STATE_ACTS:
            return f"{indent}％（{category}）[{subject}]＝{outline}"
        elif act in THINKING_ACTS:
            return f"{indent}（{category}）[{subject}]{outline}"
        elif act in SELECT_ACTS:
            if ActType.CHOICE is act:
                return f"{indent}！（{category}）[{subject}]＝{outline}"
            else:
                assert ActType.SELECTION is act
                selects = outline.replace(' ','').split(',')
                _selects = '/'.join(selects)
                return f'{indent}？（{category}）[{subject}]＝{_selects}'
        elif act in TIME_ACTS:
            return f"[XII] {outline}"
        else:
            logger.warning(
                    msg.ERR_FAIL_INVALID_DATA_WITH_DATA.format(data=f"act type in format: {PROC}"),
                    act)
            return None

    def _to_comment(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        return markdown_comment_style_of(record.subject)

    def _to_flag(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        act = assertion.is_instance(record.act, ActType)
        category = record.act.to_category()
        subject = record.subject
        outline = record.outline
        indent = get_indent(2)

        if ActType.FORESHADOW is act:
            return f"<{subject}>＝{outline}"
        else:
            return f"<{subject}>〜{outline}"

    def _to_light(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        outline = record.outline

        if outline.isnumeric():
            lux = int(outline)
            dark = 10 - lux
            _lux = '□' * lux
            _dark = '■' * dark
            return f"[{_lux}{_dark}]"
        else:
            return None

    def _to_object(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        subject = record.subject

        if subject:
            return f"[{subject}]"
        else:
            return None

    def _to_person(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        subject = record.subject

        if subject:
            return f">>{subject}"
        else:
            return None

    def _to_sky(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        return f"//空：{record.outline}//"

    def _to_spin(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        info = assertion.is_instance(record.note, SpinInfo)

        camera = info.subject
        stage = info.stage
        location = info.location
        year = info.year
        date = info.date
        time = info.time
        clock = info.clock

        return f"○{stage}/{location}（{time}/{clock}） - {date}/{year} - [{camera}]"

    def _to_symbol(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        return f"{record.outline}"

    def _to_time(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        return f"[＋] {record.outline}"

    def _to_title(record: StructRecord) -> str:
        assert isinstance(record, StructRecord)

        head = '#' + '#' * int(record.note) if record.note != -1 else ''
        index = record.outline
        return f"{head} {index}. {record.subject}"


# Private Functions
def _get_person_tags(callings: dict) -> list:
    assert isinstance(callings, dict)

    return [k for k in callings.keys()]
