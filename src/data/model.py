from dataclasses import dataclass
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from calc import score


@dataclass
class Model:
    mass: float
    pull: float
    constant_current: float
    voltage: float
    maxes: dict[str, float]
    bias: int
    discharge: float
    multiplier: float
    version: str

    def __init__(
        self,
        mass: float,
        pull: float,
        constant_current: float,
        voltage: float,
        bias: int,
        discharge: float,
        multiplier: float,
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
        self.multiplier = multiplier
        self.version = version

    def __repr__(self):
        return json.dumps(__dict__)

    @staticmethod
    def load(self, json_str: str) -> Model:
        data = json.loads(json_str)
        return Model(
            data.mass,
            data.pull,
            data.constant_current,
            data.voltage,
            data.bias,
            data.discharge,
            data.multiplier,
            data.version,
            p_max=data.maxes.p,
            i_max=data.maxes.i,
        )

    def save(self, output: str, dpi: float, format: str, transparent: bool) -> None:
        if not os.path.exists(output):
            os.mkdirs(output)
            with open(f"{output}/model.json", "w") as outfile:
                outfile.write(self.__repr__())
        self.save_graph(output, dpi, format, transparent)

    def save_graph(
        self, output: str, dpi: float, format: str, transparent: bool
    ) -> None:
        X = np.arange(0, 12, 0.1)
        y = np.array([score(x, self) for x in X])

        ax = plt.axes()
        plt.plot(X, y)
        ax.set_xlabel("Capacity (Ah)")
        ax.set_ylabel("Flight Time (mins)")
        plt.savefig(
            f"{output}/model.png", dpi=dpi, format=format, transparent=transparent
        )

    def adjust(
        self,
        mass: float,
        pull: float,
        constant_current: float,
        voltage: float,
        bias: int,
        p_max: float,
        i_max: float,
        discharge: float,
        multiplier: float,
    ) -> None:
        self.mass = mass if mass != None else self.mass
        self.pull = pull if pull != None else self.pull
        self.constant_current = (
            constant_current if constant_current != None else self.constant_current
        )
        self.voltage = voltage if voltage != None else self.voltage
        self.p_max = p_max if p_max != None else self.p_max
        self.i_max = i_max if i_max != None else self.i_max
        self.bias = bias if bias != None else self.bias
        self.discharge = discharge if discharge != None else self.discharge
        self.multiplier = multiplier if multiplier != None else self.multiplier
