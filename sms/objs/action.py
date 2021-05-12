"""Define action code object."""

# Official Libraries
from __future__ import annotations


# My Modules
from sms.objs.basecode import BaseCode
from sms.types.action import ActType
from sms.utils import assertion


__all__ = (
        'Action',
        )


# Main
class Action(BaseCode):

    def __init__(self, type: ActType, subject: str, outline: str,
            descs: list = None, note: str = None):
        self.type = assertion.is_instance(type, ActType)
        self.subject = assertion.is_str(subject)
        self.outline = assertion.is_str(outline)
        self.descs = assertion.is_list(descs) if descs else []
        self.note = assertion.is_str(note) if note else ''

    def add(self, val: str) -> bool:
        assert isinstance(val, str)

        self.descs.append(val)

        return True

    def cloned(self) -> Action:
        return Action(self.type,
                self.subject,
                self.outline,
                [d for d in self.descs] if self.descs else [],
                self.note)

    def inherited(self,
            type: ActType = None,
            subject: str = None,
            outline: str = None,
            descs: list = None,
            note: str = None,
            ) -> Action:
        return Action(
                assertion.is_instance(type, ActType) if type else self.type,
                assertion.is_str(subject) if subject else self.subject,
                assertion.is_str(outline) if outline else self.outline,
                assertion.is_list(descs) if descs else self.descs,
                assertion.is_str(note) if note else self.note,
                )
