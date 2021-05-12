"""Define story data."""

# Official Libraries


# My Modules
from sms.utils import assertion


__all__ = (
        'StoryData',
        )


# Main
class StoryData(object):

    def __init__(self, data: list):
        self.data = assertion.is_list(data)

    def get_data(self) -> list:
        return self.data

    def is_empty(self) -> bool:
        return True if not self.data else False
