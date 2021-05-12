"""Define action code object."""

# Official Libraries
from __future__ import annotations
from typing import Any


# My Modules
from sms.objs.basecode import BaseCode
from sms.types.instruction import InstType
from sms.utils import assertion


__all__ = (
        'Instruction',
        )


# Main
class Instruction(BaseCode):

    def __init__(self, type: InstType, args: list = None, note: str = None):
        self.type = assertion.is_instance(type, InstType)
        self.args = assertion.is_list(args) if args else []
        self.note = assertion.is_str(note) if note else ''

    def add(self, val: Any) -> bool:

        self.args.append(val)

        return True

    def cloned(self) -> Instruction:
        return Instruction(
                self.type,
                [a for a in self.args] if self.args else [],
                self.note)
