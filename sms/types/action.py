"""Define action type."""

# Official Libraries
from enum import auto, Enum


__all__ = (
        'ActType',
        )


# Main
class ActType(Enum):
    NONE = auto()
    # normal
    DO = auto()
    # person
    BE = auto()
    COME = auto()
    GO = auto()
    FACE = auto()
    WEAR = auto()
    FEEL = auto()
    # object
    HAVE = auto()
    PUT = auto()
    RID = auto()
    # view
    DRAW = auto()
    EXPLAIN = auto()
    SKY = auto()
    # dialogue
    TALK = auto()
    THINK = auto()
    VOICE = auto()
    # data
    PLOT = auto()
    FORESHADOW = auto()
    PAYOFF = auto()
    # symbol
    TITLE = auto()
    NOTE = auto()
    MARK = auto()
    BR = auto()
    SAME = auto()

    def to_checker(self) -> tuple:
        return {
                ActType.BE: ('be'),
                ActType.BR: ('br'),
                ActType.COME: ('come'),
                ActType.DO: ('do'),
                ActType.DRAW: ('draw'),
                ActType.EXPLAIN: ('explain'),
                ActType.FACE: ('face'),
                ActType.FEEL: ('feel'),
                ActType.FORESHADOW: ('foreshadow', 'FS'),
                ActType.GO: ('go'),
                ActType.HAVE: ('have'),
                ActType.MARK: ('mark'),
                ActType.NONE: ('none'),
                ActType.NOTE: ('note'),
                ActType.PAYOFF: ('payoff', 'PO'),
                ActType.PLOT: ('plot'),
                ActType.PUT: ('put'),
                ActType.RID: ('rid'),
                ActType.SAME: ('same', '-'),
                ActType.SKY: ('sky'),
                ActType.TALK: ('talk'),
                ActType.THINK: ('think'),
                ActType.TITLE: ('title'),
                ActType.VOICE: ('voice'),
                ActType.WEAR: ('wear'),
                }[self]


NORMAL_ACTION = [
        ActType.BE,
        ActType.COME,
        ActType.DO,
        ActType.DRAW,
        ActType.EXPLAIN,
        ActType.FACE,
        ActType.FEEL,
        ActType.GO,
        ActType.TALK,
        ActType.THINK,
        ActType.VOICE,
        ActType.WEAR,
        ]


OBJECT_ACTS = [
        ActType.PUT,
        ActType.RID,
        ]


NO_SUBJECT_ACTS = [
        ActType.SKY,
        ActType.NOTE,
        ActType.PLOT,
        ]
