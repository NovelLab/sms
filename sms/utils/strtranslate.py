"""String translate utility."""

# Official Libraries
import re


__all__ = (
        'translate_tags_str',
        'translate_tags_text_list',
        )


# Main
def translate_tags_str(text: str, tags: dict, is_fullmatch: bool = False,
        prefix: str = '$') -> str:
    assert isinstance(text, str)
    assert isinstance(tags, dict)
    assert isinstance(is_fullmatch, bool)

    if prefix:
        assert isinstance(prefix, str)
        return _conv_text_by_tag_with_prefix(text, tags, is_fullmatch, prefix)
    else:
        return _conv_text_by_tag(text, tags, is_fullmatch)


def translate_tags_text_list(textlist: list, tags: dict) -> list:
    assert isinstance(textlist, list)
    assert isinstance(tags, dict)

    tmp = []

    for line in textlist:
        assert isinstance(line, str)
        tmp.append(_conv_text_by_tag_with_prefix(line, tags))

    return tmp


# Private Functions
def _conv_text_by_tag(text: str, tags: dict, is_fullmatch: bool = False) -> str:
    assert isinstance(text, str)
    assert isinstance(tags, dict)
    assert isinstance(is_fullmatch, bool)

    tmp = text

    for key, val in tags.items():
        if is_fullmatch and key == tmp or not is_fullmatch and key in tmp:
            tmp = re.sub(r'{}'.format(key), val, tmp)
    return tmp


def _conv_text_by_tag_with_prefix(text: str, tags: dict, is_fullmatch: bool = False, prefix: str = '$') -> str:
    assert isinstance(text, str)
    assert isinstance(tags, dict)
    assert isinstance(is_fullmatch, bool)
    assert isinstance(prefix, str)

    tmp = text

    for key, val in tags.items():
        if prefix in tmp:
            tag_key = f"{prefix}{key}"
            if is_fullmatch and tag_key == tmp or not is_fullmatch and tag_key in tmp:
                tmp = re.sub(r'\{}'.format(tag_key), val, tmp)
    return tmp
