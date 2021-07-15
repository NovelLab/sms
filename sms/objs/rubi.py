"""Define rubi object."""

# Official Libraries


# My Modules
from sms.objs.baseobject import SObject
from sms.utils import assertion


__all__ = (
        'Rubi',
        'RubiData',
        )


# Main
class Rubi(SObject):

    def __init__(self, tag: str, name: str):
        super().__init__(tag, name)
        self.exclusions = []
        self.is_always = False
        self._done = False

    def done(self):
        self._done = True

    def is_done(self) -> bool:
        return self._done


class RubiData(SObject):

    def __init__(self):
        super().__init__('__RUBI', 'ルビ')
        self.data = {}

    def append(self, key: str, val: Rubi):
        self.data[key] = assertion.is_instance(val, Rubi)
