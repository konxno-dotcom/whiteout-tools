
from whiteout_tools.data import PACKS
from whiteout_tools.models.target import Target
from whiteout_tools.optimizer.craftsman_shop import CraftsmanShopOptimizer


def test_group_by_price() -> None:
    optimizer = CraftsmanShopOptimizer(PACKS)

    groups = optimizer._group_by_price()

    assert len(groups) == 5

    assert len(groups[800]) == 3
    assert len(groups[1600]) == 3
    assert len(groups[3200]) == 3
    assert len(groups[8000]) == 3
    assert len(groups[15800]) == 3


def test_first_tier_only() -> None:
    optimizer = CraftsmanShopOptimizer(PACKS)

    result = optimizer.optimize(
        Target(
            alloy=20000,
            polish=200,
            blueprint=0,
        )
    )

    assert result.total_price == 800

def test_second_tier() -> None:
    optimizer = CraftsmanShopOptimizer(PACKS)

    result = optimizer.optimize(
        Target(
            alloy=40000,
            polish=400,
            blueprint=90,
        )
    )

    assert result.total_price == 2400
    assert len(result.packs) == 2

def test_search_empty_target() -> None:
    optimizer = CraftsmanShopOptimizer(PACKS)

    result = optimizer._search(
        groups=optimizer._group_by_price(),
        tier_index=0,
        selected=[],
        target=Target(
            alloy=0,
            polish=0,
            blueprint=0,
        ),
    )

    assert result.total_price == 0
    assert result.packs == []

def test_stop_when_target_reached_at_first_tier() -> None:
    optimizer = CraftsmanShopOptimizer(PACKS)

    result = optimizer.optimize(
        Target(
            alloy=20000,
            polish=200,
            blueprint=0,
        )
    )

    assert result.total_price == 800
    assert len(result.packs) == 1

def test_same_price_choose_less_surplus() -> None:
    optimizer = CraftsmanShopOptimizer(PACKS)

    result = optimizer.optimize(
        Target(
            alloy=49000,
            polish=490,
            blueprint=90,
        )
    )

    assert result.total_price == 2400
    assert result.total_alloy >= 49000
    assert result.total_polish >= 490
    assert result.total_blueprint >= 90