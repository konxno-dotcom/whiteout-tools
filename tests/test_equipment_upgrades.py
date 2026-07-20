from whiteout_tools.data.equipment_upgrades import EQUIPMENT_UPGRADES
from whiteout_tools.services.equipment_upgrade_calculator import (
    calculate_equipment_upgrade_cost,
)


def test_calculate_single_upgrade_cost() -> None:
    cost = calculate_equipment_upgrade_cost(
        upgrades=EQUIPMENT_UPGRADES,
        current_order=1,
        target_order=2,
    )

    assert cost.alloy == 3800
    assert cost.polish == 40
    assert cost.blueprint == 0
    assert cost.moon_amber == 0


def test_calculate_multiple_upgrade_costs() -> None:
    cost = calculate_equipment_upgrade_cost(
        upgrades=EQUIPMENT_UPGRADES,
        current_order=1,
        target_order=4,
    )

    assert cost.alloy == 3800 + 7000 + 9700
    assert cost.polish == 40 + 70 + 95
    assert cost.blueprint == 0
    assert cost.moon_amber == 0


def test_same_level_cost_is_zero() -> None:
    cost = calculate_equipment_upgrade_cost(
        upgrades=EQUIPMENT_UPGRADES,
        current_order=10,
        target_order=10,
    )

    assert cost.alloy == 0
    assert cost.polish == 0
    assert cost.blueprint == 0
    assert cost.moon_amber == 0