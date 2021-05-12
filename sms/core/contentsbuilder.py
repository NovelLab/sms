"""Contents build module."""

# Official Libraries
from dataclasses import dataclass


# My Modules
from sms.commons.format import get_br, get_breakline
from sms.commons.format import get_indent
from sms.db.outputsdata import OutputsData
from sms.db.storydata import StoryData
from sms.objs.basecode import BaseCode
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.utils.log import logger
from sms.utils.strtranslate import translate_tags_text_list


__all__ = (
        'build_contents',
        )


# Define Constants
PROC = 'BUILD CONTENTS'


@dataclass
class ContentRecord(object):
    level: int
    title: str


# Main
def build_contents(story_data: StoryData, tags: dict) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []

    for record in story_data.get_data():
        assert isinstance(record, BaseCode)
        if isinstance(record, SceneInfo):
            ret = Converter.to_content_record(record)
            if ret:
                tmp.append(ret)
        else:
            continue

    formatted = Formatter.format_data(tmp)
    if not formatted:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"format data: {PROC}"))
        return None

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return OutputsData(translated)


# Processes
class Converter(object):

    def to_content_record(info: SceneInfo) -> ContentRecord:
        assert isinstance(info, SceneInfo)

        return ContentRecord(
                info.level,
                info.title,
                )


class Formatter(object):

    @classmethod
    def format_data(cls, data: list) -> list:
        assert isinstance(data, list)

        _PROC = f"{PROC}: format"
        logger.debug(msg.PROC_START.format(proc=_PROC))

        tmp = []
        indices = [0]

        for record in data:
            assert isinstance(record, ContentRecord)
            ret = None
            if record.level == 0:
                ret = cls.conv_main_title(record)
            else:
                if record.level >= len(indices):
                    indices.append(0)
                ret = cls.conv_content_title(indices, record)
            if ret:
                tmp.append(ret)
                tmp.append(get_br())

        tmp.append(get_breakline())

        logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

        return tmp

    def conv_content_title(indices: list, record: ContentRecord) -> str:
        assert isinstance(indices, list)
        assert isinstance(record, ContentRecord)

        indices[record.level] += 1
        index = indices[record.level]
        head = f"{get_indent(record.level - 1, '    ')}{index}. "

        return f"{head}{record.title}"

    def conv_main_title(record: ContentRecord) -> str:
        assert isinstance(record, ContentRecord)

        return f"{record.title}\n===\n\n"
