"""Define asset type."""

# Official Libraries
from enum import Enum


__all__ = (
        'AssetType',
        )


# Main
class AssetType(Enum):
    NONE = 'none'
    PERSON = 'person'
    STAGE = 'stage'
    ITEM = 'item'
    # special
    MOB = 'mob'
    TIME = 'time'
    WORD = 'word'
    RUBI = 'rubi'

    def __str__(self) -> str:
        return self.value
