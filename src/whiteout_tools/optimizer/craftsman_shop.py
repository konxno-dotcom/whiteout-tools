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
            groups=groups,
            tier_index=0,
            selected=[],
            target=target,
            current_alloy=0,
            current_polish=0,
            current_blueprint=0,
            current_price=0,
        )

    def _search(
        self,
        groups: dict[int, list[Pack]],
        tier_index: int,
        selected: list[Pack],
        target: Target,
        current_alloy: int,
        current_polish: int,
        current_blueprint: int,
        current_price: int,
    ) -> OptimizationResult:
        is_reached = (
            current_alloy >= target.alloy
            and current_polish >= target.polish
            and current_blueprint >= target.blueprint
        )

        current_result = OptimizationResult(
            packs=selected.copy(),
            total_price=current_price,
            is_reached=is_reached,
        )

        if is_reached:
            return current_result

        if tier_index >= len(self.PRICE_TIERS):
            return current_result

        price = self.PRICE_TIERS[tier_index]
        best_result: OptimizationResult | None = None

        for pack in groups[price]:
            candidate = self._search(
                groups=groups,
                tier_index=tier_index + 1,
                selected=[*selected, pack],
                target=target,
                current_alloy=current_alloy + pack.alloy,
                current_polish=current_polish + pack.polish,
                current_blueprint=current_blueprint + pack.blueprint,
                current_price=current_price + pack.price_tier,
            )

            if self._is_better_result(candidate, best_result, target):
                best_result = candidate

        return best_result if best_result is not None else current_result

    def _group_by_price(self) -> dict[int, list[Pack]]:
        groups: dict[int, list[Pack]] = {}

        for pack in self._packs:
            groups.setdefault(pack.price_tier, []).append(pack)

        return groups

    def _is_target_reached(self, packs: list[Pack], target: Target) -> bool:
        return (
            sum(pack.alloy for pack in packs) >= target.alloy
            and sum(pack.polish for pack in packs) >= target.polish
            and sum(pack.blueprint for pack in packs) >= target.blueprint
        )

    def _surplus_score(
        self,
        result: OptimizationResult,
        target: Target,
    ) -> int:
        surplus_alloy = max(0, result.total_alloy - target.alloy)
        surplus_polish = max(0, result.total_polish - target.polish)
        surplus_blueprint = max(0, result.total_blueprint - target.blueprint)

        # 合金10,000 = 研磨剤100 = 図面20
        return (
            surplus_alloy
            + surplus_polish * 100
            + surplus_blueprint * 500
        )

    def _shortage_score(
        self,
        result: OptimizationResult,
        target: Target,
    ) -> int:
        shortage_alloy = max(0, target.alloy - result.total_alloy)
        shortage_polish = max(0, target.polish - result.total_polish)
        shortage_blueprint = max(0, target.blueprint - result.total_blueprint)

        # 合金10,000 = 研磨剤100 = 図面20
        return (
        shortage_alloy
        + shortage_polish * 100
        + shortage_blueprint * 500
    )

    def _is_better_result(
        self,
        candidate: OptimizationResult,
        current_best: OptimizationResult | None,
        target: Target,
    ) -> bool:
        if current_best is None:
            return True

        if candidate.is_reached and not current_best.is_reached:
            return True

        if not candidate.is_reached and current_best.is_reached:
            return False

        if not candidate.is_reached and not current_best.is_reached:
            candidate_shortage = self._shortage_score(candidate, target)
            current_shortage = self._shortage_score(current_best, target)

            if candidate_shortage != current_shortage:
                return candidate_shortage < current_shortage

        if candidate.total_price < current_best.total_price:
            return True

        if candidate.total_price > current_best.total_price:
            return False

        return self._surplus_score(candidate, target) < self._surplus_score(
            current_best,
            target,
        )