from whiteout_tools.models.pack import Pack
from whiteout_tools.models.pack_category import PackCategory  # type: ignore

SEIKO_PACKS = [
    Pack(PackCategory.SEIKO, 800, 11600, 116, 48),
    Pack(PackCategory.SEIKO, 1600, 23200, 232, 96),
    Pack(PackCategory.SEIKO, 3200, 46400, 464, 192),
    Pack(PackCategory.SEIKO, 8000, 116000, 1160, 480),
    Pack(PackCategory.SEIKO, 15800, 520000, 2320, 960),
]