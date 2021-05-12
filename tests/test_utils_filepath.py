"""Test for file path utility."""

# Official Libraries
import pytest


# My Modules
from sms.utils.filepath import add_extention
from sms.utils.filepath import basename_of


# test "add_extention"
@pytest.mark.parametrize(
        ['fname', 'ext', 'expect'],
        [
            ['apple', 'txt', 'apple.txt'],
            ['orange.com', 'md', 'orange.com.md'],
            ])
def test_add_extention(fname, ext, expect):

    assert add_extention(fname, ext) == expect


# test "basenamse_of"
@pytest.mark.parametrize(
        ['fname', 'expect'],
        [
            ['apple.txt', 'apple'],
            ['border/mango.md', 'mango'],
            ['fruits/red/berry.py', 'berry'],
            ])
def test_basename_of(fname, expect):

    assert basename_of(fname) == expect
