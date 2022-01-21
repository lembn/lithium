from __future__ import annotations

import json
import os
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import output


class Model:
    # TODO: get better default value
    multipliers: dict[str, np.double] = {"lipo": 0.06519803031807178, "li-ion": 0.072}
    compounds: list[str] = list(multipliers.keys())
    F_MAX: float = 0.85  # TODO get more accurate value
    MAX_GRAPH_CAPACITY: float = 12
    GRAPH_CAPACITY_STEP: float = 0.1

    name: str
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
        name: str,
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
        self.name = name
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
                "name": self.name,
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
        )

    @staticmethod
    def load(json_str: str) -> Model:
        try:
            data = json.loads(json_str)
            return Model(
                data["name"],
                data["mass"],
                data["pull"],
                data["constant_current"],
                data["voltage"],
                data["bias"],
                data["discharge"],
                data["compound"],
                data["version"],
                p_max=data["maxes"]["p"],
                i_max=data["maxes"]["i"],
            )
        except json.JSONDecodeError:
            output.msg("ERROR - invalid JSON\nRolling back...", "red")

    def save(self, output: str, dpi: float, format: str, transparent: bool) -> None:
        output = os.path.abspath(output)
        if not os.path.exists(output):
            os.makedirs(output)
        with open(f"{output}/model.json", "w") as outfile:
            outfile.write(repr(self))
        x, y, fmax = self.points(plot_f=True)
        with open(f"{output}/meta.json", "w") as outfile:
            capacity, mass, _ = self.solve(Model.F_MAX, False)
            outfile.write(
                json.dumps(
                    {
                        "f-base": y[0],  # y intercept of f graph
                        "f-gradient": self.multipliers[self.compound]
                        / self.pull,  # gradient of f graph
                        "c-max": x[-1],  # maximum capacity
                        "non-red": (fmax - y[0])
                        / (1 - y[0]),  # percentage of the graph that isn't red
                        "longest": {
                            "capacity": capacity,
                            "mass": mass,
                        },  # specs of longest flying battery
                    },
                    indent=4,
                )
            )
        self.save_graph(output, dpi, format, transparent)

    # TODO this method does too much. It saves and returns
    def save_graph(
        self, outfile: str, dpi: float, format: str, transparent: bool
    ) -> None:
        axs = output.get_axs()

        x, y, fmax = self.points()
        axs[0].plot(np.array(x), np.array(y), color="k")
        axs[0].axvline(fmax, linestyle="--", color="k", alpha=0.4)
        axs[0].axvspan(fmax, x[-1], color="r", alpha=0.2, hatch="/")
        axs[0].set_ylabel("Flight Time (mins)")

        x, y, fmax = self.points(plot_f=True)
        axs[1].plot(np.array(x), np.array(y), color="k")
        axs[1].axhline(fmax, linestyle="--", color="k", alpha=0.4)
        axs[1].axhspan(fmax, y[-1], color="r", alpha=0.2, hatch="\\")
        axs[1].set_xlabel("Capacity (Ah)")
        axs[1].set_ylabel("F")

        plt.savefig(
            f"{outfile}/model.png", dpi=dpi, format=format, transparent=transparent
        )

    def points(self, plot_f: bool = False):
        X = []
        Y = []
        fmax = -1
        for x in np.arange(0, Model.MAX_GRAPH_CAPACITY, Model.GRAPH_CAPACITY_STEP):
            if plot_f:
                y = self.get_f(x)
            else:
                y, f = self.model(x)
            test = y if plot_f else f
            if test > 1:
                break
            if test > Model.F_MAX and fmax == -1:
                fmax = y if plot_f else x
            X.append(x)
            Y.append(y)
        return X, Y, fmax

    def get_f(self, capacity: float, battery_mass: float = 0) -> float:
        if battery_mass == 0:
            battery_mass = Model.multipliers[self.compound] * capacity
        return (battery_mass + self.mass + 0.005 * self.bias) / self.pull

    def model(self, capacity: float, battery_mass: float = 0) -> tuple[float, float]:
        total = 0
        denominator = 0

        f = self.get_f(capacity, battery_mass)
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

        return total / denominator * 60, f

    def solve(self, ftarget: float, override: bool) -> tuple[float, float]:
        if (ftarget > Model.F_MAX or ftarget <= 0) and not override:
            ftarget = Model.F_MAX

        capacity = (
            self.pull * ftarget - 0.005 * self.bias - self.mass
        ) / Model.multipliers[self.compound]

        return capacity, Model.multipliers[self.compound] * capacity, ftarget
