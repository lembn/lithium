from money import Money
from typing import Callable
from dataclasses import dataclass, field

currency = {"£": "GPB", "$": "USD"}


@dataclass
class Battery:
    score: int = field(default=0)
    id: str = field(default=None)
    capacity: float = field(default=None)
    mass: float = field(default=None)
    link: str = field(default=None)
    price: Money = field(default=None)

    def __init__(self, id: str, capacity: str, mass: str, link: str, price: str):
        self.id = id
        self.capacity = float(capacity) / 1000
        self.mass = float(mass) / 1000
        self.link = link
        self.price = Money(price, currency[price[0]])

    def setScore(self, score: Callable[[Battery], float]) -> None:
        self.score = score(self)

    @staticmethod
    def empty() -> Battery:
        return Battery("", 0, 0, "", None)
