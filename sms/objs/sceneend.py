"""Define scene info object for end."""

# Official Libraries


# My Modules
from sms.objs.basecode import BaseCode
from sms.utils import assertion


__all__ = (
        'SceneEnd',
        )


# Main
class SceneEnd(BaseCode):

    def __init__(self, tag: str):
        self.tag = assertion.is_str(tag)
