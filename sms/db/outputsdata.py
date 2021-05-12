"""Define outputs data."""

# Official Libraries
from __future__ import annotations


# My Modules
from sms.utils import assertion


__all__ = (
        'OutputsData',
        )


# Main
class OutputsData(object):

    def __init__(self, data: list):
        self.data = assertion.is_list(data)

    def cloned(self) -> OutputsData:
        return OutputsData([d for d in self.data])

    def get_data(self) -> list:
        return self.data

    def get_serialized_data(self) -> str:
        return "".join(self.data)

    def is_empty(self) -> bool:
        return True if not self.data else False

    def __add__(self, another: OutputsData) -> OutputsData:
        assert isinstance(another, OutputsData)

        self.data = self.data + another.data

        return self
