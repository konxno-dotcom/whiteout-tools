import csv
from pathlib import Path

from whiteout_tools.models.equipment_upgrade import EquipmentUpgrade

CSV_PATH = Path(__file__).with_name("equipment_upgrade.csv")


def load_equipment_upgrades() -> list[EquipmentUpgrade]:
    """領主装備の強化データをCSVから読み込む"""

    upgrades: list[EquipmentUpgrade] = []

    with CSV_PATH.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            upgrades.append(
                EquipmentUpgrade(
                    order=int(row["order"]),
                    name=row["name"],
                    alloy=int(row["alloy"]),
                    polish=int(row["polish"]),
                    blueprint=int(row["blueprint"]),
                    moon_amber=int(row["moon_amber"]),
                )
            )

    return upgrades


EQUIPMENT_UPGRADES = load_equipment_upgrades()