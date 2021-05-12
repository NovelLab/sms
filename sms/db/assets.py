"""Define asset db."""

# Official Libraries


# My Modules
from sms.db.base import BaseDB
from sms.objs.baseobject import SObject


__all__ = (
        'AssetsDB',
        )


# Main
class AssetsDB(BaseDB):

    def __init__(self):
        super().__init__(SObject)
