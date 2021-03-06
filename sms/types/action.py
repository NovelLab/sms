"""Define action type."""

# Official Libraries
from enum import auto, Enum


__all__ = (
        'ActType',
        'NORMAL_ACTS',
        'OBJECT_ACTS',
        'NO_SUBJECT_ACTS',
        'FLAG_ACTS',
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
    DISCARD = auto()
    HAVE = auto()
    PUT = auto()
    RID = auto()
    # view
    DRAW = auto()
    EXPLAIN = auto()
    SKY = auto()
    LIGHT = auto()
    # dialogue
    TALK = auto()
    THINK = auto()
    VOICE = auto()
    # info
    HEAR = auto()
    KNOW = auto()
    OCCUR = auto()
    PROMISE = auto()
    REMEMBER = auto()
    STATE = auto()
    WHY = auto()
    SELECTION = auto()
    CHOICE = auto()
    # food
    EAT = auto()
    DRINK = auto()
    # time
    ELAPSE = auto()
    # data
    PLOT = auto()
    FORESHADOW = auto()
    PAYOFF = auto()
    # symbol
    TITLE = auto()
    NOTE = auto()
    MARK = auto()
    BR = auto()
    PLAIN = auto()
    SAME = auto()

    def to_checker(self) -> tuple:
        return {
                ActType.BE: ('be'),
                ActType.BR: ('br'),
                ActType.CHOICE: ('choice',),
                ActType.COME: ('come'),
                ActType.DISCARD: ('discard', 'dis'),
                ActType.DO: ('do', 'D'),
                ActType.DRAW: ('draw', 'R'),
                ActType.DRINK: ('drink'),
                ActType.EAT: ('eat'),
                ActType.ELAPSE: ('elapse'),
                ActType.EXPLAIN: ('explain', 'X'),
                ActType.FACE: ('face'),
                ActType.FEEL: ('feel'),
                ActType.FORESHADOW: ('foreshadow', 'FS'),
                ActType.GO: ('go'),
                ActType.HAVE: ('have'),
                ActType.HEAR: ('hear'),
                ActType.KNOW: ('know'),
                ActType.LIGHT: ('light',),
                ActType.MARK: ('mark'),
                ActType.NONE: ('none'),
                ActType.NOTE: ('note'),
                ActType.OCCUR: ('occur'),
                ActType.PAYOFF: ('payoff', 'PO'),
                ActType.PLAIN: ('plain', 'P'),
                ActType.PLOT: ('plot'),
                ActType.PROMISE: ('promise', 'prom'),
                ActType.PUT: ('put'),
                ActType.REMEMBER: ('remember', 'rem'),
                ActType.RID: ('rid'),
                ActType.SAME: ('same', '-'),
                ActType.SELECTION: ('selection', 'sel'),
                ActType.SKY: ('sky'),
                ActType.STATE: ('state',),
                ActType.TALK: ('talk', 'T'),
                ActType.THINK: ('think', 'K'),
                ActType.TITLE: ('title'),
                ActType.VOICE: ('voice'),
                ActType.WEAR: ('wear'),
                ActType.WHY: ('why'),
                }[self]

    def to_category(self) -> str:
        return {
                ActType.BE: '??????',
                ActType.BR: '??????',
                ActType.CHOICE: '??????',
                ActType.COME: '??????',
                ActType.DISCARD: '??????',
                ActType.DO: '??????',
                ActType.DRAW: '??????',
                ActType.DRINK: '??????',
                ActType.EAT: '?????????',
                ActType.ELAPSE: '????????????',
                ActType.EXPLAIN: '??????',
                ActType.FACE: '??????',
                ActType.FEEL: '??????',
                ActType.FORESHADOW: '??????',
                ActType.GO: '??????',
                ActType.HAVE: '??????',
                ActType.HEAR: '??????',
                ActType.KNOW: '??????',
                ActType.LIGHT: '??????',
                ActType.MARK: '??????',
                ActType.NONE: '??????',
                ActType.NOTE: '??????',
                ActType.OCCUR: '??????',
                ActType.PAYOFF: '??????',
                ActType.PLOT: '??????',
                ActType.PROMISE: '??????',
                ActType.PUT: '??????',
                ActType.REMEMBER: '????????????',
                ActType.RID: '??????',
                ActType.SAME: '??????',
                ActType.SELECTION: '?????????',
                ActType.SKY: '???',
                ActType.STATE: '??????',
                ActType.TALK: '??????',
                ActType.THINK: '??????',
                ActType.TITLE: '??????',
                ActType.VOICE: '??????',
                ActType.WEAR: '??????',
                ActType.WHY:'??????',
                }[self]


NORMAL_ACTS = [
        ActType.BE,
        ActType.CHOICE,
        ActType.COME,
        ActType.DISCARD,
        ActType.DO,
        ActType.DRAW,
        ActType.DRINK,
        ActType.EAT,
        ActType.EXPLAIN,
        ActType.FACE,
        ActType.FEEL,
        ActType.GO,
        ActType.HAVE,
        ActType.HEAR,
        ActType.KNOW,
        ActType.OCCUR,
        ActType.PROMISE,
        ActType.REMEMBER,
        ActType.SELECTION,
        ActType.STATE,
        ActType.TALK,
        ActType.THINK,
        ActType.VOICE,
        ActType.WEAR,
        ActType.WHY,
        ]


OBJECT_ACTS = [
        ActType.PUT,
        ActType.RID,
        ]


NO_SUBJECT_ACTS = [
        ActType.SKY,
        ActType.LIGHT,
        ActType.ELAPSE,
        ActType.NOTE,
        ActType.PLOT,
        ActType.MARK,
        ]


FLAG_ACTS = [
        ActType.FORESHADOW,
        ActType.PAYOFF,
        ]


SYMBOL_ACTS = [
        ActType.BR,
        ActType.MARK,
        ActType.NONE,
        ActType.NOTE,
        ActType.PLOT,
        ActType.PLAIN,
        ActType.SAME,
        ActType.TITLE,
        ]
