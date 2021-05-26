"""Convert module for next and after day."""

# Official Libraries


# My Modules
from sms.objs.basecode import BaseCode
from sms.objs.sceneinfo import SceneInfo
from sms.syss import messages as msg
from sms.utils.datetimes import after_day_str_from
from sms.utils.log import logger


__all__ = (
        'apply_scene_info_next',
        )


# Define Constants
PROC = 'NEXT CONV'


# Main
def apply_scene_info_next(data: list) -> list:
    assert isinstance(data, list)

    _PROC = f"{PROC}: scene info next conv"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    cache = None

    for record in data:
        assert isinstance(record, BaseCode)
        if isinstance(record, SceneInfo):
            ret = Converter.conv_next_day(record, cache)
            if ret:
                tmp.append(ret)
                cache = ret
            else:
                tmp.append(record)
        else:
            tmp.append(record)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return tmp


# Processes
class Converter(object):

    @classmethod
    def conv_next_day(cls, info: SceneInfo, cache: SceneInfo) -> SceneInfo:
        assert isinstance(info, SceneInfo)

        if 'nospin' in info.flags:
            return None

        if cache:
            assert isinstance(cache, SceneInfo)
        else:
            return info

        year = info.year
        if cls._is_same(info.year):
            year = cache.year
        elif cls._is_next(info.year):
            year = cls._next_year_from(cache.year, info.year)
        elif cls._is_after(info.year):
            year = cls._after_year_from(cache.year, info.year)

        date = info.date
        if cls._is_same(info.date):
            date = cache.date
        elif cls._is_next(info.date):
            date = cls._next_date_from(int(year), cache.date, info.date)
        elif cls._is_after(info.date):
            date = cls._after_date_from(int(year), cache.date, info.date)

        time = info.time
        if cls._is_same(info.time):
            time = cache.time
        elif cls._is_next(info.time):
            time = cls._next_time_from(cache.time, info.time)
        elif cls._is_after(info.time):
            time = cls._after_time_from(cache.time, info.time)

        # TODO: clock next?

        return SceneInfo(
                info.level,
                info.tag,
                info.title,
                info.camera,
                info.stage,
                info.location,
                str(year),
                str(date),
                str(time),
                info.clock,
                info.outline,
                info.flags,
                info.note,
                )

    def _after_date_from(base: str, data: str) -> str:
        assert isinstance(base, str)
        assert isinstance(data, str)

        logger.debug(msg.MSG_UNIMPLEMENT_PROC.format(proc=f"after date unimplement: {PROC}"))

        return base

    def _after_time_from(base: str, data: str) -> str:
        assert isinstance(base, str)
        assert isinstance(data, str)

        logger.debug(msg.MSG_UNIMPLEMENT_PROC.format(proc=f"after time unimplement: {PROC}"))

        if ':' in base:
            return base
        else:
            return base

    def _after_year_from(base: str, data: str) -> int:
        assert isinstance(base, str)
        assert isinstance(data, str)

        addition = data.replace('after', '')
        return int(base) + int(addition)

    def _is_after(text: str) -> bool:
        assert isinstance(text, str)

        if text:
            if text in ['afternoon', 'afterschool']:
                return False
            else:
                return 'after' in text
        else:
            return False

    def _is_next(text: str) -> bool:
        assert isinstance(text, str)

        if text:
            return 'next' in text
        else:
            return False

    def _is_same(text: str) -> bool:
        assert isinstance(text, str)

        if text:
            return text in ('same', '-')
        else:
            return False

    def _next_date_from(year: int, base: str, data: str) -> str:
        assert isinstance(year, int)
        assert isinstance(base, str)
        assert isinstance(data, str)

        mon, day = base.split('/')

        if 'mon' in data:
            addition = data.replace('mon', '').replace('next', '')
            _addition = int(addition) if addition else 1
            return after_day_str_from(year, mon, day, _addition, 0)
        elif 'day' in data:
            addition = data.replace('day', '').replace('next', '')
            _addition = int(addition) if addition else 1
            return after_day_str_from(year, mon, day, 0, _addition)
        elif 'week' in data:
            addition = data.replace('week', '').replace('next', '')
            _addition = int(addition) if addition else 1
            return after_day_str_from(year, mon, day, 0, 7 * _addition)
        else:
            return after_day_str_from(year, mon, day, 0, 1)

    def _next_time_from(base: str, data: str) -> str:
        assert isinstance(base, str)
        assert isinstance(data, str)

        logger.debug(msg.MSG_UNIMPLEMENT_PROC.format(proc=f"next time unimplement: {PROC}"))

        if ':' in base:
            return base
        else:
            return base

    def _next_year_from(base: str, data: str) -> int:
        assert isinstance(base, str)
        assert isinstance(data, str)

        addition = data.replace('next', '')
        _addition = int(addition) if addition else 1

        return int(base) + _addition
