from money import Money

currency = {"£": "GBP", "$": "USD"}


class Battery:
    score: float = float("-inf")
    id: str = None
    capacity: float = None
    mass: float = None
    link: str = None
    price: Money = None

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
