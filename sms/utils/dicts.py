"""Utility module for dictonary."""


# Official Libraries


# My Modules


__all__ = (
        'combine_dicts',
        'dict_sorted',
        )


# Main
def combine_dicts(dict_a: dict, dict_b: dict)  -> dict:
    assert isinstance(dict_a, dict)
    assert isinstance(dict_b, dict)

    return dict(dict_a, **dict_b)


def dict_sorted(src: dict, is_reverse: bool=False) -> dict:
    """Convert the dictionary data to sorted data."""
    assert isinstance(src, dict)
    assert isinstance(is_reverse, bool)

    return dict(sorted(src.items(), key=lambda x: x[0], reverse=is_reverse))
