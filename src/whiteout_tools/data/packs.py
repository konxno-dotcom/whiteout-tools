from whiteout_tools.models.pack import Pack
from whiteout_tools.models.pack_category import PackCategory  # type: ignore

PACKS: list[Pack] = [
    Pack(
        category=PackCategory.MYOGI,
        tier=800,
        alloy=26000,
        polish=262,
        blueprint=0,
    ),
    Pack(
        category=PackCategory.MYOGI,
        tier=1600,
        alloy=52000,
        polish=524,
        blueprint=0,
    ),
    Pack(
        category=PackCategory.MYOGI,
        tier=3200,
        alloy=104000,
        polish=1048,
        blueprint=0,
    ),
]