"""Define scene codes db."""

# Official Libraries


# My Modules
from sms.db.base import BaseDB
from sms.objs.scenecode import SceneCode


__all__ = (
        'ScenesDB',
        )


# Main
class ScenesDB(BaseDB):

    def __init__(self):
        super().__init__(SceneCode)
