from dataclasses import dataclass

from whiteout_tools.models.pack import Pack


@dataclass(slots=True)
class OptimizationResult:
    """最適化結果"""

    packs: list[Pack]
    total_price: int

    @property
    def total_alloy(self) -> int:
        return sum(p.alloy for p in self.packs)

    @property
    def total_polish(self) -> int:
        return sum(p.polish for p in self.packs)

    @property
    def total_blueprint(self) -> int:
        return sum(p.blueprint for p in self.packs)