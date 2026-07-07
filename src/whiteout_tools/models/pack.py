from dataclasses import dataclass

from whiteout_tools.models.pack_category import PackCategory  # type: ignore


@property
def value(self) -> tuple[int, int, int]:
    return (self.alloy, self.polish, self.blueprint)

@dataclass(slots=True, frozen=True)
class Pack:
    """ゲーム内パック"""

    category: PackCategory
    price_tier: int

    alloy: int
    polish: int
    blueprint: int