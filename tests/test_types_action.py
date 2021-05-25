"""Test for type of action."""

# Official Libraries
import pytest


# My Modules
from sms.types.action import ActType


# test "act type coverage check"
def test_ActType_to_checker_has_all_type():

    for act in ActType:
        assert act.to_checker()
