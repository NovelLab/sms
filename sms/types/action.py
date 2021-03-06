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
                ActType.BE: 'いる',
                ActType.BR: '改行',
                ActType.CHOICE: '選ぶ',
                ActType.COME: '来る',
                ActType.DISCARD: '廃棄',
                ActType.DO: '行動',
                ActType.DRAW: '描画',
                ActType.DRINK: '飲む',
                ActType.EAT: '食べる',
                ActType.ELAPSE: '時間経過',
                ActType.EXPLAIN: '説明',
                ActType.FACE: '表情',
                ActType.FEEL: '感情',
                ActType.FORESHADOW: '伏線',
                ActType.GO: '行く',
                ActType.HAVE: '持つ',
                ActType.HEAR: '聞く',
                ActType.KNOW: '知る',
                ActType.LIGHT: '光量',
                ActType.MARK: '記号',
                ActType.NONE: 'なし',
                ActType.NOTE: '備考',
                ActType.OCCUR: '発生',
                ActType.PAYOFF: '回収',
                ActType.PLOT: 'ＰＬ',
                ActType.PROMISE: '約束',
                ActType.PUT: '設置',
                ActType.REMEMBER: '思い出す',
                ActType.RID: '削除',
                ActType.SAME: '同じ',
                ActType.SELECTION: '選択肢',
                ActType.SKY: '空',
                ActType.STATE: '状態',
                ActType.TALK: '会話',
                ActType.THINK: '思考',
                ActType.TITLE: 'ＴＴ',
                ActType.VOICE: '音声',
                ActType.WEAR: '衣装',
                ActType.WHY:'疑問',
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
