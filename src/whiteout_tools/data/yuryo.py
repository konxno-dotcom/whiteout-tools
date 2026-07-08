from whiteout_tools.models.pack import Pack
from whiteout_tools.models.pack_category import PackCategory  # type: ignore

YURYO_PACKS = [
    Pack(PackCategory.YURYO, 800, 1, 7200, 72, 78),
    Pack(PackCategory.YURYO, 1600, 2, 14400, 144, 156),
    Pack(PackCategory.YURYO, 3200, 3, 28800, 288, 312),
    Pack(PackCategory.YURYO, 8000, 4, 72000, 720, 780),
    Pack(PackCategory.YURYO, 15800, 5, 144000, 1440, 1560),
]