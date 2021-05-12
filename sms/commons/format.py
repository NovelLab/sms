"""Format module."""

# Official Libraries


# My Modules
from sms.syss import messages as msg
from sms.utils.log import logger


__all__ = (
        'get_br',
        'get_breakline',
        'get_indent',
        'join_descs',
        'markdown_comment_style_of',
        )


# Define Constants
PROC = 'COMMON FORMAT'


# Main
def get_br(num: int = 1) -> str:
    return '\n' * num


def get_breakline() -> str:
    return "--------" * 8 + '\n'


def get_indent(num: int, parts: str = '　') -> str:
    assert isinstance(num, int)
    assert isinstance(parts, str)

    return parts * num


def join_descs(descs: list) -> str:
    assert isinstance(descs, list)

    tmp = ''

    for line in descs:
        assert isinstance(line, str)
        _ = line if line.endswith(('。', '、', '」', '』', '？', '！')) else line + '。'
        tmp += _
    return tmp


def markdown_comment_style_of(text: str) -> str:
    assert isinstance(text, str)

    return f"<!--{text}-->\n"
