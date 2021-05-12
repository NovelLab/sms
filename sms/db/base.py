"""Define base db object class."""

# Official Libraries
from typing import Any
from typing import T


# My Modules


__all__ = (
        'BaseDB',
        )


# Main
class BaseDB(object):

    def __init__(self, use_type: T):
        self.data = {}
        self._type = use_type

    def add(self, key: str, val: Any) -> bool:
        assert isinstance(key, str)
        assert isinstance(val, self._type)

        self.data[key] = val

        return True

    def get(self, key: str) -> T:
        assert isinstance(key, str)

        return self.data[key]

    def has(self, key: str) -> bool:
        assert isinstance(key, str)

        return key in self.data

    def is_empty(self) -> bool:
        return True if not self.data else False
