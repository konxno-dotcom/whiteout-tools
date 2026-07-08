from whiteout_tools.data import PACKS
from whiteout_tools.models.target import Target
from whiteout_tools.optimizer.brute_force import BruteForceOptimizer
from whiteout_tools.optimizer.craftsman_shop import CraftsmanShopOptimizer


def test_optimize_empty_target() -> None:
    optimizer = BruteForceOptimizer(PACKS)

    result = optimizer.optimize(
        Target(
            alloy=0,
            polish=0,
            blueprint=0,
        )
    )

    assert result.total_price == 0
    assert result.packs == []



def test_single_pack() -> None:
    optimizer = BruteForceOptimizer(PACKS)

    result = optimizer.optimize(
        Target(
            alloy=10000,
            polish=100,
            blueprint=40,
        )
    )

    assert result.total_price == 800
    assert len(result.packs) == 1



def test_two_packs() -> None:
    optimizer = BruteForceOptimizer(PACKS)

    result = optimizer.optimize(
        Target(
            alloy=70000,
            polish=700,
            blueprint=140,
        )
    )

    assert result.total_price == 4000
    assert len(result.packs) == 2

def test_need_second_tier() -> None:
    optimizer = CraftsmanShopOptimizer(PACKS)  # noqa: F821

    result = optimizer.optimize(
        Target(
            alloy=30000,
            polish=300,
            blueprint=50,
        )
    )

    assert len(result.packs) == 2
    assert result.total_price == 2400

def test_real_case_large_target() -> None:
    optimizer = CraftsmanShopOptimizer(PACKS)

    result = optimizer.optimize(
        Target(
            alloy=100_000,
            polish=3_800,
            blueprint=1_600,
        )
    )

    assert result.total_price > 0

    assert result.total_alloy >= 100_000
    assert result.total_polish >= 3_800
    assert result.total_blueprint >= 1_600


