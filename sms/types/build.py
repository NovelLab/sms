"""Define build type."""

# Official Libraries
from enum import auto, Enum


__all__ = (
        'BuildType',
        )


# Main
class BuildType(Enum):
    NONE = auto()
    OUTLINE = auto()
    PLOT = auto()
    STRUCT = auto()
    SCRIPT = auto()
    NOVEL = auto()
    INFO = auto()
