"""Define basic story object."""

# Official Libraries


# My Modules
from sms.utils import assertion


__all__ = (
        'SObject',
        )


# Main
class SObject(object):

    def __init__(self, tag: str, name: str):
        self.tag = assertion.is_str(tag)
        self.name = assertion.is_str(name)
