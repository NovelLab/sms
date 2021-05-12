"""Define raw source data object."""

# Official Libraries
from dataclasses import dataclass, field


# My Modules
from sms.utils import assertion


__all__ = (
        'RawSrc',
        )


# Main
@dataclass
class RawSrc(object):
    tag: str
    data: list = field(default_factory=list)
