from whiteout_tools.models.result import OptimizationResult
from whiteout_tools.models.target import Target


class BruteForceOptimizer:
    """総当たり最適化"""

    def optimize(self, target: Target) -> OptimizationResult:
        raise NotImplementedError