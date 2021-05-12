"""Utility module for date and time controls."""


# Official Libraries
import datetime
from typing import Union

# Thirdparty Libraries
from dateutil.relativedelta import relativedelta


# My Modules


__all__ = (
        'after_day_str_from',
        'next_day_str_from',
        'next_month_str_from',
        )

INT_STR = Union[int, str]

# Main Functions
def after_day_str_from(year: INT_STR, mon: INT_STR, day: INT_STR,
        aftermon: int, afterday: int) -> str:
    assert isinstance(year, (int, str))
    assert isinstance(mon, (int, str))
    assert isinstance(day, (int, str))
    assert isinstance(aftermon, int)
    assert isinstance(afterday, int)

    basedate = datetime.date(int(year), int(mon), int(day))
    elapsed = basedate + relativedelta(months=aftermon, days=afterday)

    return str(elapsed.month) + '/' + str(elapsed.day)


def next_day_str_from(year: INT_STR, mon: INT_STR, day: INT_STR) -> str:
    return after_day_str_from(year, mon, day, 0, 1)


def next_month_str_from(year: INT_STR, mon: INT_STR, day: INT_STR) -> str:
    return after_day_str_from(year, mon, day, 1, 0)
