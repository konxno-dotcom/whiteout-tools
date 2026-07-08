from dataclasses import dataclass

from whiteout_tools.models.pack import Pack


@dataclass(slots=True)
class Purchase:
    """購入したパック"""

    pack: Pack
    quantity: int = 1

    @property
    def total_price(self) -> int:
        return self.pack.price_tier * self.quantity

    @property
    def total_alloy(self) -> int:
        return self.pack.alloy * self.quantity

    @property
    def total_polish(self) -> int:
        return self.pack.polish * self.quantity

    @property
    def total_blueprint(self) -> int:
        return self.pack.blueprint * self.quantity