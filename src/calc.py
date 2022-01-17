from data.model import Model


def score_battery(capacity: float, mass: float, model: Model) -> float:
    def clip(x: float) -> float:
        if x <= 0:
            return 0
        elif x >= 1:
            return 1
        else:
            return x

    total = 0
    denominator = 0
    f = clip(mass + model.mass / model.pull + 0.001 * model.bias)
    if model.maxes["p"] > 0:
        total += (capacity * model.discharge) / (
            model.constant_current + f * model.maxes["p"] / model.voltage
        )
        denominator += 1
    if model.maxes["i"] > 0:
        total += (capacity * model.discharge) / (
            model.constant_current + f * model.maxes["i"]
        )
        denominator += 1

    return total / denominator * 60


def score(capacity: float, model: Model) -> float:
    def clip(x: float) -> float:
        if x <= 0:
            return 0
        elif x >= 1:
            return 1
        else:
            return x

    total = 0
    denominator = 0
    f = clip(
        (model.multiplier * capacity + model.mass) / model.pull + 0.001 * model.bias
    )
    if model.maxes["p"] > 0:
        total += (capacity * model.discharge) / (
            model.constant_current
            + (f * model.maxes["p"]) / round(3.7 * model.cells, 1)
        )
        denominator += 1
    if model.maxes["i"] > 0:
        total += (capacity * model.discharge) / (
            model.constant_current + f * model.maxes["i"]
        )
        denominator += 1

    return total / denominator * 60
