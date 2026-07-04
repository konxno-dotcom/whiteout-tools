from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Pack:
    """ゲーム内パック"""

    category: str
    tier: int

    alloy: int
    polish: int
    blueprint: int