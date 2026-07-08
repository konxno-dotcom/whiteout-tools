from whiteout_tools.data import PACKS
from whiteout_tools.rules import is_valid_selection


def test_same_step_is_invalid() -> None:
    packs = [
        PACKS[0],   # 妙技800
        PACKS[5],   # 精巧800
    ]

    assert not is_valid_selection(packs)


def test_different_steps_are_valid() -> None:
    packs = [
        PACKS[0],   # 妙技800
        PACKS[6],   # 精巧1600
    ]

    assert is_valid_selection(packs)