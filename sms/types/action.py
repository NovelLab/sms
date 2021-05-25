"""Define action type."""

# Official Libraries
from enum import auto, Enum


__all__ = (
        'ActType',
        'NORMAL_ACTS',
        'OBJECT_ACTS',
        'NO_SUBJECT_ACTS',
        'FALG_ACTS',
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
    KNOW = auto()
    PROMISE = auto()
    REMEMBER = auto()
    STATE = auto()
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
                ActType.DISCARD: ('discard', 'dis'),
                ActType.DO: ('do'),
                ActType.DRAW: ('draw'),
                ActType.EXPLAIN: ('explain'),
                ActType.FACE: ('face'),
                ActType.FEEL: ('feel'),
                ActType.FORESHADOW: ('foreshadow', 'FS'),
                ActType.GO: ('go'),
                ActType.HAVE: ('have'),
                ActType.KNOW: ('know'),
                ActType.LIGHT: ('light',),
                ActType.MARK: ('mark'),
                ActType.NONE: ('none'),
                ActType.NOTE: ('note'),
                ActType.PAYOFF: ('payoff', 'PO'),
                ActType.PLOT: ('plot'),
                ActType.PROMISE: ('promise', 'prom'),
                ActType.PUT: ('put'),
                ActType.REMEMBER: ('remember', 'rem'),
                ActType.RID: ('rid'),
                ActType.SAME: ('same', '-'),
                ActType.SKY: ('sky'),
                ActType.STATE: ('state',),
                ActType.TALK: ('talk'),
                ActType.THINK: ('think'),
                ActType.TITLE: ('title'),
                ActType.VOICE: ('voice'),
                ActType.WEAR: ('wear'),
                }[self]

    def to_category(self) -> str:
        return {
                ActType.BE: 'いる',
                ActType.BR: '改行',
                ActType.COME: '来る',
                ActType.DISCARD: '廃棄',
                ActType.DO: '行動',
                ActType.DRAW: '描画',
                ActType.EXPLAIN: '説明',
                ActType.FACE: '表情',
                ActType.FEEL: '感情',
                ActType.FORESHADOW: '伏線',
                ActType.GO: '行く',
                ActType.HAVE: '持つ',
                ActType.KNOW: '知る',
                ActType.LIGHT: '光量',
                ActType.MARK: '記号',
                ActType.NONE: 'なし',
                ActType.NOTE: '備考',
                ActType.PAYOFF: '回収',
                ActType.PLOT: 'ＰＬ',
                ActType.PROMISE: '約束',
                ActType.PUT: '設置',
                ActType.REMEMBER: '想起',
                ActType.RID: '削除',
                ActType.SAME: '同じ',
                ActType.SKY: '空',
                ActType.STATE: '状態',
                ActType.TALK: '会話',
                ActType.THINK: '思考',
                ActType.TITLE: 'ＴＴ',
                ActType.VOICE: '音声',
                ActType.WEAR: '衣装',
                }[self]


NORMAL_ACTS = [
        ActType.BE,
        ActType.COME,
        ActType.DISCARD,
        ActType.DO,
        ActType.DRAW,
        ActType.EXPLAIN,
        ActType.FACE,
        ActType.FEEL,
        ActType.GO,
        ActType.HAVE,
        ActType.KNOW,
        ActType.PROMISE,
        ActType.REMEMBER,
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
        ActType.LIGHT,
        ActType.NOTE,
        ActType.PLOT,
        ActType.MARK,
        ]


FLAG_ACTS = [
        ActType.FORESHADOW,
        ActType.PAYOFF,
        ]
