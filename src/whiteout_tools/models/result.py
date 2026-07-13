from dataclasses import dataclass

from whiteout_tools.models.pack import Pack


@dataclass(slots=True)
class OptimizationResult:
    """最適化結果"""

    packs: list[Pack]
    total_price: int
    is_reached: bool = True

    @property
    def total_alloy(self) -> int:
        return sum(pack.alloy for pack in self.packs)

    @property
    def total_polish(self) -> int:
        return sum(pack.polish for pack in self.packs)

    @property
    def total_blueprint(self) -> int:
        return sum(pack.blueprint for pack in self.packs)