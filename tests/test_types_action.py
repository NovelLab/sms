"""Test for type of action."""

# Official Libraries
import pytest


# My Modules
from sms.types.action import ActType
from sms.types.action import SYMBOL_ACTS
from sms.core.structbuilder import DIALOGUE_ACTS
from sms.core.structbuilder import DOING_ACTS
from sms.core.structbuilder import DRAW_ACTS
from sms.core.structbuilder import FLAG_ACTS
from sms.core.structbuilder import STATE_ACTS
from sms.core.structbuilder import SELECT_ACTS
from sms.core.structbuilder import THINKING_ACTS
from sms.core.structbuilder import TIME_ACTS


# test "act type coverage check"
def test_ActType_to_checker_has_all_type():

    for act in ActType:
        assert act.to_checker()


def test_ActType_covered_in_structbuilder():

    def _checker(act: ActType) -> bool:
        assert isinstance(act, ActType)

        for a in DIALOGUE_ACTS + DOING_ACTS + DRAW_ACTS + FLAG_ACTS + STATE_ACTS + SELECT_ACTS + THINKING_ACTS + TIME_ACTS + SYMBOL_ACTS:
            if act is a:
                return True
        return False

    for act in ActType:
        assert _checker(act)
