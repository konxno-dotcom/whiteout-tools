from whiteout_tools.models.target import Target


def test_target_create() -> None:
    target = Target(
        alloy=100_000,
        polish=3_800,
        blueprint=1_600,
    )

    assert target.alloy == 100_000
    assert target.polish == 3_800
    assert target.blueprint == 1_600
    