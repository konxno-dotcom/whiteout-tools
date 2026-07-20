from dataclasses import dataclass

from whiteout_tools.models.equipment_upgrade import EquipmentUpgrade


@dataclass(slots=True, frozen=True)
class EquipmentUpgradeCost:
    """指定範囲の装備強化に必要な合計素材"""

    alloy: int
    polish: int
    blueprint: int
    moon_amber: int


def calculate_equipment_upgrade_cost(
    upgrades: list[EquipmentUpgrade],
    current_order: int,
    target_order: int,
) -> EquipmentUpgradeCost:
    """現在段階の次から、目標段階までの必要素材を合計する"""

    if target_order <= current_order:
        return EquipmentUpgradeCost(
            alloy=0,
            polish=0,
            blueprint=0,
            moon_amber=0,
        )

    selected_upgrades = [
        upgrade
        for upgrade in upgrades
        if current_order < upgrade.order <= target_order
    ]

    return EquipmentUpgradeCost(
        alloy=sum(upgrade.alloy for upgrade in selected_upgrades),
        polish=sum(upgrade.polish for upgrade in selected_upgrades),
        blueprint=sum(upgrade.blueprint for upgrade in selected_upgrades),
        moon_amber=sum(upgrade.moon_amber for upgrade in selected_upgrades),
    )