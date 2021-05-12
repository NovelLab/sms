"""Define item object."""

# Official Libraries


# My Modules
from sms.objs.baseobject import SObject


__all__ = (
        'Item',
        )


# Main
class Item(SObject):

    def __init__(self, tag: str, name: str):
        super().__init__(tag, name)
        self.note = None
