"""Build outline module."""

# Official Libraries
from dataclasses import dataclass


# My Modules
from sms.commons.format import get_br, get_breakline
from sms.db.outputsdata import OutputsData
from sms.db.storydata import StoryData
from sms.objs.basecode import BaseCode
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.utils.log import logger
from sms.utils.dicts import dict_sorted
from sms.utils.strings import get_indent_text
from sms.utils.strtranslate import translate_tags_text_list


__all__ = (
        'build_outline',
        )


# Define Constants
PROC = 'BUILD OUTLINE'


@dataclass
class OutlineRecord(object):
    level: int
    index: int
    title: str
    outline: str


# Main
def build_outline(story_data: StoryData, tags: dict) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    outlines = Converter.outlines_data_from(story_data)
    if not outlines:
        return None

    reordered = Converter.reorder_outlines(outlines)
    if not reordered:
        return None

    formatted = Formatter.format_data(reordered)
    if not formatted:
        return None

    translated = translate_tags_text_list(formatted, dict_sorted(tags, True))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return OutputsData(translated)


# Processes
class Converter(object):

    @classmethod
    def outlines_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []

        for record in story_data.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, SceneInfo):
                ret = cls._to_outline_record(record)
                if ret:
                    tmp.append(ret)
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted outlines data: {PROC}"))

        return tmp

    @classmethod
    def reorder_outlines(cls, data: list) -> list:
        assert isinstance(data, list)

        tmp = []

        maxlevel = cls._get_deepest_level(data)

        for level in range(maxlevel + 1):
            index = 1
            for record in data:
                assert isinstance(record, OutlineRecord)
                if level == record.level:
                    tmp.append(cls._update_index(index, record))
                    index += 1

        logger.debug(msg.PROC_MESSAGE.format(proc=f"reordered outlines data: {PROC}"))

        return tmp

    def _get_deepest_level(data: list) -> int:
        assert isinstance(data, list)

        level = 0
        for record in data:
            assert isinstance(record, OutlineRecord)
            if level < record.level:
                level = record.level

        return level

    def _to_outline_record(record: SceneInfo) -> OutlineRecord:
        assert isinstance(record, SceneInfo)

        return OutlineRecord(
                record.level,
                0,
                record.title,
                record.outline)

    def _update_index(index: int, record: OutlineRecord) -> OutlineRecord:
        assert isinstance(index, int)
        assert isinstance(record, OutlineRecord)

        return OutlineRecord(
                record.level,
                index,
                record.title,
                record.outline)


class Formatter(object):

    @classmethod
    def format_data(cls, data: list) -> list:
        assert isinstance(data, list)

        tmp = []
        current = 0

        for record in data:
            assert isinstance(record, OutlineRecord)
            if current != record.level:
                tmp.append(get_breakline())
                current = record.level
            ret = cls._to_output_record(record)
            if ret:
                tmp.extend(ret)
                tmp.append(get_br(2))

        logger.debug(msg.PROC_MESSAGE.format(proc=f"formatted outlines data: {PROC}"))

        return tmp

    def _to_output_record(record: OutlineRecord) -> list:
        assert isinstance(record, OutlineRecord)

        outline = get_indent_text(record.outline)

        return [f"{record.index}. {record.title}\n",
                outline]
