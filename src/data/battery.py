from money import Money
from typing import Callable
from dataclasses import dataclass, field

currency = {"£": "GBP", "$": "USD"}


@dataclass
class Battery:
    score: float = field(default=float("-inf"))
    id: str = field(default=None)
    capacity: float = field(default=None)
    mass: float = field(default=None)
    link: str = field(default=None)
    price: Money = field(default=None)

    def __init__(
        self, id: str, capacity: str, mass: str, link: str, price: str
    ) -> None:
        self.id = id
        self.capacity = float(capacity) / 1000
        self.mass = float(mass) / 1000
        self.link = link
        self.price = Money(price[1:], currency[price[0]])

    @staticmethod
    def empty():
        return Battery("", 0, 0, "", None)
