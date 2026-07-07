from whiteout_tools.data import PACKS


def test_total_alloy() -> None:
    assert sum(p.alloy for p in PACKS) == (
        962000 +
        429200 +
        26640
    )



def test_pack_count() -> None:
    assert len(PACKS) == 15