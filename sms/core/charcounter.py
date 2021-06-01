"""Char count module."""

# Official Libraries
import re
from dataclasses import dataclass

# My Modules
from sms.commons.format import get_br, get_breakline
from sms.syss import messages as msg
from sms.types.build import BuildType
from sms.utils.counts import count_lines_by_columns, count_white_space
from sms.utils.log import logger
from sms.utils.strings import just_string_of, rid_rn

__all__ = (
        'char_counts_from',
        )


# Define Constants
PROC = 'CHAR COUNTER'


@dataclass
class CountRecord(object):
    level: int
    title: str
    total: int
    space: int
    lines: float
    papers: float


TITLE_PREFIX = re.compile(r'^[0-9]+\. ')

NOVEL_TITLE_PREFIX = re.compile(r'^#+ ')


# Main
def char_counts_from(type: BuildType, data: list, columns: int, rows: int) -> list:
    assert isinstance(type, BuildType)
    assert isinstance(data, list)
    assert isinstance(columns, int)
    assert isinstance(rows, int)

    logger.debug(msg.PROC_START.format(proc=PROC))

    counts = CharCounter.counts_data_from(type, data, columns, rows)
    if not counts:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"'{type}' char counts data: {PROC}"))
        return None

    formatted = Formatter.format_data(type, counts)
    if not formatted:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"format '{type}' counts data: {PROC}"))
        return None

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return formatted


# Processes
class CharCounter(object):

    @classmethod
    def counts_data_from(cls, type: BuildType,
            data: list, columns: int, rows: int) -> list:
        assert isinstance(type, BuildType)
        assert isinstance(data, list)
        assert isinstance(columns, int)
        assert isinstance(rows, int)

        if type in [BuildType.OUTLINE, BuildType.PLOT]:
            return cls._counts_outline_from(type, data, columns, rows)
        elif type in [BuildType.SCRIPT, BuildType.NOVEL, BuildType.STRUCT]:
            return cls._counts_data_from(type, data, columns, rows)
        else:
            return []

    @classmethod
    def _counts_data_from(cls, type: BuildType,
            data: list, columns: int, rows: int) -> list:
        assert isinstance(type, BuildType)
        assert isinstance(data, list)
        assert isinstance(columns, int)
        assert isinstance(rows, int)

        tmp = []
        indices = [0]
        titles = [['']]
        descs = [['']]

        for record in data:
            assert isinstance(record, str)
            if record.startswith('#'):
                # scene head
                level = record.count('#')
                if len(indices) <= level:
                    indices.append(0)
                    titles.append([''])
                    descs.append([''])
                indices[level] += 1
                titles[level].append(cls._title_from(record))
                descs[level].append('#')
            elif re.search(r'[0-9]+\.', record):
                # scene head in outline and plot
                pass
            elif record.startswith('<!--'):
                # comment
                continue
            elif record.startswith('----'):
                # breakline
                continue
            elif BuildType.STRUCT is type and record.startswith('['):
                # spin info
                continue
            elif BuildType.STRUCT is type and record.startswith('>>'):
                # person info
                continue
            else:
                # text
                for level in range(len(indices)):
                    descs[level][indices[level]] += rid_rn(record)

        for level in range(len(indices)):
            tmp.extend(Converter.counts_from(
                level,
                titles[level],
                descs[level],
                columns, rows))

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted '{type}' char count data: {PROC}"))

        return tmp

    @classmethod
    def _counts_outline_from(cls, type: BuildType,
            data: list, columns: int, rows: int) -> list:
        assert isinstance(type, BuildType)
        assert isinstance(data, list)
        assert isinstance(columns, int)
        assert isinstance(rows, int)

        tmp = []
        indices = [0]
        titles = [['']]
        descs = [['']]
        level = 0
        cur_index = 0

        for record in data:
            assert isinstance(record, str)
            if record.startswith('----'):
                # change level
                level += 1
                if len(indices) <= level:
                    indices.append(0)
                    titles.append([''])
                    descs.append([''])
            elif re.search(TITLE_PREFIX, record):
                # scene head in outline
                indices[level] += 1
                titles[level].append(rid_rn(record))
                descs[level].append('')
            elif record.startswith('#'):
                # novel scene head
                continue
            elif record.startswith('<!--'):
                # comment
                continue
            elif record.startswith('** '):
                # sub title
                continue
            else:
                # text
                for level in range(len(indices)):
                    descs[level][indices[level]] += rid_rn(record)

        for level in range(len(indices)):
            tmp.extend(Converter.counts_from(
                level,
                titles[level],
                descs[level],
                columns, rows))

        logger.debug(msg.PROC_MESSAGE.format(proc=f"converted '{type}' char count data: {PROC}"))
        return tmp

    def _title_from(record: str) -> str:
        assert isinstance(record, str)

        return re.sub(NOVEL_TITLE_PREFIX, '', record)


class Converter(object):

    @classmethod
    def counts_from(cls, level: int, titles: list, descs: list,
            columns: int, rows: int) -> list:
        assert isinstance(level, int)
        assert isinstance(titles, list)
        assert isinstance(descs, list)
        assert isinstance(columns, int)
        assert isinstance(rows, int)

        tmp = []

        for title, text in zip(titles[1:], descs[1:]):
            tmp.append(cls._record_from(level, title, text, columns, rows))

        return tmp

    def _record_from(level: int, title: str, text: str,
            columns: int, rows: int) -> CountRecord:
        assert isinstance(level, int)
        assert isinstance(title, str)
        assert isinstance(text, str)
        assert isinstance(columns, int)
        assert isinstance(rows, int)

        lines = count_lines_by_columns(text, columns)

        return CountRecord(level, title, len(text), count_white_space(text),
                lines, lines / rows)


class Formatter(object):

    @classmethod
    def format_data(cls, type: BuildType, data: list) -> list:
        assert isinstance(type, BuildType)
        assert isinstance(data, list)

        tmp = []
        current = 0

        tmp.append(cls._title_of(type))
        tmp.append(get_br(2))

        for record in data:
            assert isinstance(record, CountRecord)
            if current != record.level:
                current = record.level
                tmp.append(get_br())
                tmp.append(get_breakline())
            tmp.append(cls._conv_count_record(record))
            tmp.append(get_br())

        tmp.append(get_br(2))

        logger.debug(msg.PROC_MESSAGE.format(proc=f"formatted '{type}' char counts data: {PROC}"))

        return tmp

    def _conv_count_record(record: CountRecord) -> str:
        assert isinstance(record, CountRecord)

        title = just_string_of(record.title, 20)
        total = record.total
        space = record.space
        real = just_string_of(str(total - space), 8, is_right=True)
        lines = just_string_of(str(round(record.lines, 3)), 8, is_right=True)
        papers = just_string_of(str(round(record.papers, 3)), 8, is_right=True)
        _total = just_string_of(str(total), 8, is_right=True)
        _space = just_string_of(str(space), 8, is_right=True)

        return f"- {title}: {papers}p/{lines}n [{_total}c ({real}/{_space})c]"

    def _title_of(type: BuildType) -> str:
        assert isinstance(type, BuildType)

        if BuildType.OUTLINE is type:
            return "## OUTLINE Char counts"
        elif BuildType.PLOT is type:
            return "## PLOT Char counts"
        elif BuildType.SCRIPT is type:
            return "## SCRIPT Char counts"
        elif BuildType.NOVEL is type:
            return "## NOVEL Char Counts"
        elif BuildType.STRUCT is type:
            return "## STRUCT Char Counts"
        else:
            return "## Char Counts"
