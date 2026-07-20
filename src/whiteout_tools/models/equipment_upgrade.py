from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EquipmentUpgrade:
    """領主装備の強化段階ごとの必要素材"""

    order: int
    name: str
    alloy: int
    polish: int
    blueprint: int
    moon_amber: int