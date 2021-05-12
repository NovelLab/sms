"""Define source db."""

# Official Libraries


# My Modules
from sms.db.base import BaseDB
from sms.objs.rawsrc import RawSrc


__all__ = (
        'SrcsDB',
        )


# Main
class SrcsDB(BaseDB):

    def __init__(self):
        super().__init__(RawSrc)
