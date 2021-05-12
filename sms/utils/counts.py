"""Count utility."""

# Official Libraries


# My Modules


__all__ = (
        'count_lines_by_columns',
        'count_white_space',
        )


# Main
def count_lines_by_columns(text: str, columns: int) -> int:
    assert isinstance(text, str)
    assert isinstance(columns, int)

    lines = text.split('\n')
    num = 0.0
    for line in lines:
        if len(line) > columns:
            num += len(line) / columns
        else:
            num += 1
    return num


def count_white_space(text: str) -> int:
    assert isinstance(text, str)

    space = 0
    for c in text:
        if c.isspace():
            space += 1
    return space
