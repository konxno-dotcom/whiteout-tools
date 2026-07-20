from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class MaterialCost:
    """強化に必要な素材数"""

    alloy: int
    polish: int
    blueprint: int