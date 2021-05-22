"""Define scene info object."""

# Official Libraries


# My Modules
from sms.objs.basecode import BaseCode
from sms.utils import assertion


__all__ = (
        'SceneInfo',
        )


# Main
class SceneInfo(BaseCode):

    def __init__(self, level: int, tag: str,
            title: str,
            camera: str, stage: str, location: (int, str),
            year: str, date: str, time: str, clock: str,
            outline: str,
            flags: (str, list),
            note: str):
        self.level = assertion.is_int(level)
        self.tag = assertion.is_str(tag)
        self.title = assertion.is_str(title) if title else ''
        self.camera = assertion.is_str(camera) if camera else ''
        self.stage = assertion.is_str(stage) if stage else ''
        self.location = 'INT'
        self.year = assertion.is_str(year) if year else ''
        self.date = assertion.is_str(date) if date else ''
        self.time = assertion.is_str(time) if time else ''
        self.clock = assertion.is_str(clock) if clock else ''
        self.outline = assertion.is_str(outline) if outline else ''
        self.flags = []
        self.note = assertion.is_str(note) if note else ''
        if location:
            if isinstance(location, str):
                self.location = 'INT' if location.lower() in ('in', 'int') else 'EXT'
            elif isinstance(location, int):
                self.location = 'INT' if location > 0 else 'EXT'
            else:
                self.location = 'INT'
        if flags:
            if isinstance(flags, str):
                self.flags = [flags]
            else:
                self.flags = assertion.is_list(flags)
