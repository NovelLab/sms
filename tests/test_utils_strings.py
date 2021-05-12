"""Test for string utility."""

# Official Libraries
import pytest


# My Modules
from sms.utils.strings import rid_head_space
from sms.utils.strings import rid_rn


# test "rid_head_space"
@pytest.mark.parametrize(
        ['src', 'expect'],
        [
            ['test', 'test'],
            [' apple', 'apple'],
            ['　orange', 'orange'],
            ['  peach', 'peach'],
            ])
def test_rid_head_space(src, expect):

    assert rid_head_space(src) == expect


# test "rid_rn"
@pytest.mark.parametrize(
        ['src', 'expect'],
        [
            ['apple\n', 'apple'],
            ['orange', 'orange'],
            ['melon\n\r', 'melon'],
            ['peach\r\n', 'peach'],
            ])
def test_rid_rn(src, expect):

    assert rid_rn(src) == expect
