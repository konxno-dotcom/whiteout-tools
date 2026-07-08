from whiteout_tools.data import PACKS
from whiteout_tools.models.pack_category import PackCategory


def test_pack_count() -> None:
    assert len(PACKS) == 15


def test_myogi_total() -> None:
    myogi = [p for p in PACKS if p.category == PackCategory.MYOGI]
    assert sum(p.alloy for p in myogi) == 962000


def test_seiko_total() -> None:
    seiko = [p for p in PACKS if p.category == PackCategory.SEIKO]
    assert sum(p.alloy for p in seiko) == 429200


def test_yuryo_total() -> None:
    yuryo = [p for p in PACKS if p.category == PackCategory.YURYO]
    assert sum(p.alloy for p in yuryo) == 266400