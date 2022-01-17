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
    cells: int
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
        cells: int,
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
        self.cells = cells
        self.maxes = {"p": p_max, "i": i_max}
        if self.maxes["p"] == float("-inf") and self.maxes["i"] == float("-inf"):
            raise AttributeError("either p-max or i-max (or both) must be defined")
        self.bias = bias
        self.discharge = discharge
        self.multiplier = multiplier
        self.version = version

    @staticmethod
    def load(path: str) -> Model:
        with open(path, "r") as infile:
            data = json.loads(infile.read())
            return Model(
                data.mass,
                data.pull,
                data.consta,
                data.cells,
                data.bias,
                data.discharge,
                data.multiplier,
                data.version,
                p_max=data.maxes.p,
                i_max=data.maxes.i,
            )

    def save(self, output: str) -> None:
        if not os.path.exists(output):
            os.mkdirs(output)

        with open(f"{output}/model.json", "w") as outfile:
            outfile.write(json.dumps(__dict__))

        X = np.arange(0, 12, 0.1)
        y = np.array([score(x, self) for x in X])

        ax = plt.axes()
        plt.plot(X, y)
        ax.set_xlabel("Capacity (Ah)")
        ax.set_ylabel("Flight Time (mins)")
        plt.savefig(f"{output}/model.png")
