"""Build plot module."""

# Official Libraries
from dataclasses import dataclass, field


# My Modules
from sms.commons.format import get_br, get_breakline
from sms.db.outputsdata import OutputsData
from sms.db.storydata import StoryData
from sms.objs.action import Action
from sms.objs.basecode import BaseCode
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.types.action import ActType
from sms.utils.log import logger
from sms.utils.dicts import dict_sorted
from sms.utils.strings import get_indent_text
from sms.utils.strtranslate import translate_tags_text_list


__all__ = (
        'build_plot',
        )


# Define Constants
PROC = 'BUILD PLOT'


@dataclass
class PlotRecord(object):
    level: int
    index: int
    title: str
    subtitle: str
    plot: list = field(default_factory=list)


# Main
def build_plot(story_data: StoryData, tags: dict) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    plots = Converter.plots_data_from(story_data)
    if not plots:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"plots data: {PROC}"))
        return None

    reordered = Converter.reorder_plots(plots)
    if not reordered:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"reordered plots: {PROC}"))
        return None

    formatted = Formatter.format_data(reordered)
    if not formatted:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"formatted plots: {PROC}"))
        return None

    translated = translate_tags_text_list(formatted, dict_sorted(tags, True))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return OutputsData(translated)


# Processes
class Converter(object):

    @classmethod
    def plots_data_from(cls, story_data: StoryData) -> list:
        assert isinstance(story_data, StoryData)

        tmp = []
        level = ''
        title = ''

        for record in story_data.get_data():
            assert isinstance(record, BaseCode)
            if isinstance(record, SceneInfo):
                level = record.level
                title = record.title
            elif isinstance(record, Action):
                ret = cls._to_plot_record(level, title, record)
                if ret:
                    tmp.append(ret)
            else:
                continue

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted plots data: {PROC}"))

        return tmp

    @classmethod
    def reorder_plots(cls, data: list) -> list:
        assert isinstance(data, list)

        tmp = []

        maxlevel = cls._get_deepest_level(data)

        for level in range(maxlevel + 1):
            index = 1
            for record in data:
                assert isinstance(record, PlotRecord)
                if level == record.level:
                    tmp.append(cls._update_index(index, record))
                    index += 1

        logger.debug(msg.PROC_MESSAGE.format(proc=f"reordered plots data: {PROC}"))

        return tmp

    def _get_deepest_level(data: list) -> int:
        assert isinstance(data, list)

        level = 0
        for record in data:
            assert isinstance(record, PlotRecord)
            if level < record.level:
                level = record.level

        return level

    def _to_plot_record(level: int, title: str, record: Action) -> PlotRecord:
        assert isinstance(level, int)
        assert isinstance(title, str)
        assert isinstance(record, Action)

        if ActType.PLOT is record.type:
            return PlotRecord(level, 0, title, record.outline, record.descs)
        else:
            return None

    def _update_index(index: int, record: PlotRecord) -> PlotRecord:
        assert isinstance(index, int)
        assert isinstance(record, PlotRecord)

        return PlotRecord(
                record.level,
                index,
                record.title,
                record.subtitle,
                record.plot)


class Formatter(object):

    @classmethod
    def format_data(cls, data: list) -> list:
        assert isinstance(data, list)

        tmp = []
        current = 0

        for record in data:
            assert isinstance(record, PlotRecord)
            if current != record.level:
                tmp.append(get_breakline())
                current = record.level
            ret = cls._to_output_record(record)
            if ret:
                tmp.extend(ret)
                tmp.append(get_br(2))

        logger.debug(msg.PROC_MESSAGE.format(proc=f"fomatted plots data: {PROC}"))

        return tmp

    def _to_output_record(record: PlotRecord) -> list:
        assert isinstance(record, PlotRecord)

        plot = get_indent_text("\n".join(record.plot))
        title = f"{record.index}. {record.title}\n"

        if record.subtitle:
            subtitle = f"** {record.subtitle} **\n"
            return [title, subtitle, plot]
        else:
            return [title, plot]
