from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Pack:
    """1つのパック"""

    category: str
    price: int

    alloy: int
    polish: int
    blueprint: int