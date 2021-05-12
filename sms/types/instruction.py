"""Define instruction type."""

# Official Libraries
from enum import auto, Enum

# My Modules


__all__ = (
        'InstType',
        )


# Main
class InstType(Enum):
    NONE = auto()
    # scene
    CALL = auto()
    # data
    ALIAS = auto()
    # control
    PARAGRAPH_START = auto()
    PARAGRAPH_END = auto()
