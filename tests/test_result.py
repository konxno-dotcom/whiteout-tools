from whiteout_tools.models.pack import Pack
from whiteout_tools.models.pack_category import PackCategory
from whiteout_tools.models.result import OptimizationResult


def test_result_total() -> None:
    packs = [
        Pack(
            category=PackCategory.MYOGI,
            price_tier=800,
            step=1,
            alloy=100,
            polish=10,
            blueprint=1,
        ),
        Pack(
            category=PackCategory.SEIKO,
            price_tier=1600,
            step=2,
            alloy=200,
            polish=20,
            blueprint=2,
        ),
    ]

    result = OptimizationResult(
        packs=packs,
        total_price=2400,
    )

    assert result.total_alloy == 300
    assert result.total_polish == 30
    assert result.total_blueprint == 3