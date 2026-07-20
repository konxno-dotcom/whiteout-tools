from whiteout_tools.models.material_cost import MaterialCost
from whiteout_tools.models.upgrade_target import UpgradeTarget

UPGRADE_TARGETS = [
    UpgradeTarget(
        name="装備レベル1 → 2",
        cost=MaterialCost(
            alloy=0,
            polish=0,
            blueprint=0,
        ),
    ),
    UpgradeTarget(
        name="装備レベル2 → 3",
        cost=MaterialCost(
            alloy=0,
            polish=0,
            blueprint=0,
        ),
    ),
]