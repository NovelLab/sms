"""Define rubi object."""

# Official Libraries


# My Modules
from sms.objs.baseobject import SObject


__all__ = (
        'Rubi',
        )


# Main
class Rubi(SObject):

    def __init__(self, tag: str, name: str):
        super().__init__(tag, name)
        self.exclusions = []
        self.is_always = False
