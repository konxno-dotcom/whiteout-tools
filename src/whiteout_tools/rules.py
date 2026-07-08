from whiteout_tools.models.pack import Pack


def is_valid_selection(packs: list[Pack]) -> bool:
    """購入可能な組み合わせか判定する"""

    used_steps: set[int] = set()

    for pack in packs:
        if pack.step in used_steps:
            return False

        used_steps.add(pack.step)

    return True