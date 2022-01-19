import click
from calc import score_battery
import numpy as np
import matplotlib.pyplot as plt
from data.model import Model


@click.command()
@click.argument("modelfiles", nargs=-1, type=click.File(mode="r"))
def show(modelfiles: tuple[str]):
    """Show the graphs of one or many models specified by MODELFILES"""

    for modelfile in modelfiles:
        model = Model.load(modelfile.read())
        X = np.arange(0, 12, 0.1)
        y = np.array([score_battery(x, model) for x in X])
        plt.plot(X, y)

    ax = plt.axes()
    ax.set_xlabel("Capacity (Ah)")
    ax.set_ylabel("Flight Time (mins)")
