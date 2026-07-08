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
    step: int

    alloy: int
    polish: int
    blueprint: int
   

Pack(PackCategory.MYOGI, 800, 1, 26000, 262, 0)
Pack(PackCategory.MYOGI, 1600, 2, 52000, 524, 0)
Pack(PackCategory.MYOGI, 3200, 3, 104000, 1048, 0)