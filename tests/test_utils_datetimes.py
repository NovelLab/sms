"""Test for date and time utility."""

# Official Libraries
import pytest

# My Modules
from sms.utils.datetimes import after_day_str_from


# test "after_day_str_from"
@pytest.mark.parametrize(
        ['year', 'mon', 'day', 'aftermon', 'afterday', 'expect'],
        [
            [2000, 1, 5, 1, 1, "2/6"],
            [2000, 1, 31, 0, 1, "2/1"],
            ])
def test_after_day_str_from(year, mon, day, aftermon, afterday, expect):

    assert after_day_str_from(year, mon, day, aftermon, afterday) == expect
