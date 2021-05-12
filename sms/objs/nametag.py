"""Define nametag object."""

# Official Libraries
from enum import Enum


# My Modules
from sms.objs.baseobject import SObject
from sms.utils import assertion


__all__ = (
        'NameTag',
        )


# Define Constants
class NameTagType(Enum):
    NONE = 'none'
    MOB = 'mob'
    TIME = 'time'
    WORD = 'word'

    def __str__(self) -> str:
        return self.value


# Main
class NameTag(SObject):

    def __init__(self, type: NameTagType, data: dict):
        super().__init__(f"__{str(type)}", '')
        self.type = assertion.is_instance(type, NameTagType)
        self.data = assertion.is_dict(data) if data else {}
