from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Target:
    """必要素材"""

    alloy: int
    polish: int
    blueprint: int