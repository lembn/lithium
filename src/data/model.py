from __future__ import annotations

import json
import os
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np


class Model:
    # TODO: get better default value
    multipliers: dict[str, float] = {"lipo": 0.072, "li-ion": 0.072}
    compounds: list[str] = list(multipliers.keys())

    mass: float
    pull: float
    constant_current: float
    voltage: float
    maxes: dict[str, float]
    bias: int
    discharge: float
    compound: Literal["lipo", "li-ion"]
    version: str

    def __init__(
        self,
        mass: float,
        pull: float,
        constant_current: float,
        voltage: float,
        bias: int,
        discharge: float,
        compound: Literal["lipo", "li-ion"],
        version: str = "1.0",
        p_max: float = float("-inf"),
        i_max: float = float("-inf"),
    ) -> None:
        self.mass = mass
        self.pull = pull
        self.constant_current = constant_current
        self.voltage = voltage
        self.maxes = {"p": p_max, "i": i_max}
        if self.maxes["p"] == float("-inf") and self.maxes["i"] == float("-inf"):
            raise AttributeError("either p-max or i-max (or both) must be defined")
        self.bias = bias
        self.discharge = discharge
        self.compound = compound
        self.version = version

    def __repr__(self):
        return json.dumps(
            {
                "mass": self.mass,
                "pull": self.pull,
                "constant_current": self.constant_current,
                "voltage": self.voltage,
                "maxes": self.maxes,
                "bias": self.bias,
                "discharge": self.discharge,
                "compound": self.compound,
                "version": self.version,
            },
            indent=4,
            sort_keys=True,
        )

    @staticmethod
    def load(json_str: str) -> Model:
        data = json.loads(json_str)
        return Model(
            data.mass,
            data.pull,
            data.constant_current,
            data.voltage,
            data.bias,
            data.discharge,
            data.version,
            p_max=data.maxes.p,
            i_max=data.maxes.i,
        )

    @staticmethod
    def clip(x: float) -> float:
        if x <= 0:
            return 0
        elif x >= 1:
            return 1
        else:
            return x

    def save(self, output: str, dpi: float, format: str, transparent: bool) -> None:
        output = os.path.abspath(output)
        if not os.path.exists(output):
            os.makedirs(output)
        with open(f"{output}/model.json", "w") as outfile:
            outfile.write(repr(self))
        self.save_graph(output, dpi, format, transparent)

    def save_graph(
        self, output: str, dpi: float, format: str, transparent: bool
    ) -> None:
        X = np.arange(0, 12, 0.1)
        y = np.array([self.model(x) for x in X])

        ax = plt.axes()
        plt.plot(X, y)
        ax.set_xlabel("Capacity (Ah)")
        ax.set_ylabel("Flight Time (mins)")
        plt.savefig(
            f"{output}/model.png", dpi=dpi, format=format, transparent=transparent
        )

    def model(self, capacity: float, mass: float = 0) -> float:
        total = 0
        denominator = 0

        if mass == 0:
            mass = Model.multipliers[self.compound] * capacity
        # f = self.clip((mass + self.mass) / self.pull + 0.001 * self.bias)
        f = (mass + self.mass) / self.pull + 0.001 * self.bias
        print(f"mass is: " + str(mass + self.mass))
        print(f"pull is: " + str(self.pull))
        print(f * 100)

        if self.maxes["p"] > 0:
            total += (capacity * self.discharge) / (
                self.constant_current + f * self.maxes["p"] / self.voltage
            )
            denominator += 1
        if self.maxes["i"] > 0:
            total += (capacity * self.discharge) / (
                self.constant_current + f * self.maxes["i"]
            )
            denominator += 1

        return total / denominator * 60
