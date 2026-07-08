from itertools import combinations

from whiteout_tools.models.pack import Pack
from whiteout_tools.models.result import OptimizationResult
from whiteout_tools.models.target import Target


class BruteForceOptimizer:
    """総当たりで最適な組み合わせを探索する"""

    def __init__(self, packs: list[Pack]) -> None:
        self._packs = packs

    def optimize(self, target: Target) -> OptimizationResult:
        # 何も必要ない場合
        if (
            target.alloy == 0
            and target.polish == 0
            and target.blueprint == 0
        ):
            return OptimizationResult(
                packs=[],
                total_price=0,
            )

        best_result: OptimizationResult | None = None

        # 1～2パックの全組み合わせを探索
        for count in (1, 2):
            for combo in combinations(self._packs, count):
                total_alloy = sum(p.alloy for p in combo)
                total_polish = sum(p.polish for p in combo)
                total_blueprint = sum(p.blueprint for p in combo)
                total_price = sum(p.price_tier for p in combo)

                if (
                    total_alloy >= target.alloy
                    and total_polish >= target.polish
                    and total_blueprint >= target.blueprint
                ):
                    if (
                        best_result is None
                        or total_price < best_result.total_price
                    ):
                        best_result = OptimizationResult(
                            packs=list(combo),
                            total_price=total_price,
                        )

        if best_result is None:
            raise NotImplementedError("3パック以上は未実装")

        return best_result