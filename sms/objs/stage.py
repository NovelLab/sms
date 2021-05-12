"""Define stage object."""

# Official Libraries


# My Modules
from sms.objs.baseobject import SObject


__all__ = (
        'Stage',
        )


# Main
class Stage(SObject):

    def __init__(self, tag: str, name: str):
        super().__init__(tag, name)
        self.note = None
