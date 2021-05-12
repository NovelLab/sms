"""Utility module for file IO."""

# Official Libraries


__all__ = (
        'read_file',
        'write_file',
        )


# Define Constants
DEFAULT_ENCODING = 'utf-8'


# Main
def read_file(fname: str, encoding: str = DEFAULT_ENCODING) -> str:
    assert isinstance(fname, str)
    assert isinstance(encoding, str)

    contents = ""

    with open(fname, 'r', encoding=encoding) as file:
        contents = file.read()

    return contents


def write_file(fname: str, contents: str,
        encoding: str = DEFAULT_ENCODING) -> bool:
    assert isinstance(fname, str)
    assert isinstance(contents, str)
    assert isinstance(encoding, str)

    with open(fname, 'w', encoding=encoding) as file:
        file.write(contents)

    return True
