from money import Money
from typing import Callable


class Battery:
    score = 0

    def __init__(self, capacity: int, mass: int, link: str, price: Money) -> None:
        self.capacity = capacity
        self.mass = mass
        self.link = link
        self.price = price

    def setScore(self, score: Callable[[Battery], float]) -> None:
        self.score = score(self)

    @staticmethod
    def empty() -> Battery:
        return Battery(0, 0, "", 0)
