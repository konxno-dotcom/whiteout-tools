from whiteout_tools.models.pack import Pack
from whiteout_tools.models.result import OptimizationResult
from whiteout_tools.models.target import Target


class CraftsmanShopOptimizer:
    """工商の匠専用Optimizer"""

    PRICE_TIERS = [800, 1600, 3200, 8000, 15800]

    def __init__(self, packs: list[Pack]) -> None:
        self._packs = packs
    def optimize(self, target: Target) -> OptimizationResult:
        groups = self._group_by_price()

        return self._search(
            groups,
            tier_index=0,
            selected=[],
            target=target,
        )

    def _group_by_price(self) -> dict[int, list[Pack]]:
        groups: dict[int, list[Pack]] = {}

        for pack in self._packs:
            groups.setdefault(pack.price_tier, []).append(pack)

        return groups
    
    def _search(
        self,
        groups: dict[int, list[Pack]],
        tier_index: int,
        selected: list[Pack],
        target: Target,
) -> OptimizationResult:
        total_alloy = sum(pack.alloy for pack in selected)
        total_polish = sum(pack.polish for pack in selected)
        total_blueprint = sum(pack.blueprint for pack in selected)
        total_price = sum(pack.price_tier for pack in selected)

        if (
            total_alloy >= target.alloy
            and total_polish >= target.polish
            and total_blueprint >= target.blueprint
    ):
            return OptimizationResult(
            packs=selected.copy(),
            total_price=total_price,
        )

        if tier_index >= len(self.PRICE_TIERS):
             raise NotImplementedError

        price = self.PRICE_TIERS[tier_index]
        best_result: OptimizationResult | None = None

        for pack in groups[price]:
            try:
                result = self._search(
                    groups=groups,
                    tier_index=tier_index + 1,
                    selected=[*selected, pack],
                    target=target,
                )
            except NotImplementedError:
                continue

            if self._is_better_result(result, best_result, target):
                best_result = result

        if best_result is None:
            raise NotImplementedError

        return best_result
    
    def _surplus_score(self, result: OptimizationResult, target: Target) -> int:
        return (
            result.total_alloy - target.alloy
            + result.total_polish - target.polish
            + result.total_blueprint - target.blueprint
    )

    def _is_better_result(
        self,
        candidate: OptimizationResult,
        current_best: OptimizationResult | None,
        target: Target,
    ) -> bool:
        if current_best is None:
            return True

        if candidate.total_price < current_best.total_price:
            return True

        if candidate.total_price > current_best.total_price:
            return False

            return self._surplus_score(candidate, target) < self._surplus_score(
                current_best,
                target,
            )