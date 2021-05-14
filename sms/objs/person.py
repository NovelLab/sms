"""Define person object."""

# Official Libraries


# My Modules
from sms.objs.baseobject import SObject


__all__ = (
        'Person',
        )


# Main
class Person(SObject):

    def __init__(self, tag: str, name: str):
        super().__init__(tag, name)
        self.fullname = None
        self.age = None
        self.sex = None
        self.job = None
        self.belong = None
        self.calling = None
        self.note = None
        self.face = None
        self.fashion = None
        self.history = None
