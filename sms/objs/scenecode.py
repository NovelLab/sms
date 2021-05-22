"""Define scene code object."""

# Official Libraries
from __future__ import annotations
from typing import Any


# My Modules
from sms.utils import assertion


__all__ = (
        'SceneCode',
        )


# Main
class SceneCode(object):

    def __init__(self, tag: str):
        self.tag = assertion.is_str(tag)
        self.data = []
        # member values
        self.title = None
        self.camera = None
        self.stage = None
        self.location = None
        self.year = None
        self.date = None
        self.time = None
        self.outline = None
        self.flags = None
        self.note = None

    def add(self, val: Any) -> bool:
        self.data.append(val)
        return True

    def get_data(self) -> list:
        return self.data

    def replace(self, data: list) -> SceneCode:
        assert isinstance(data, list)

        self.data = data
        return self
