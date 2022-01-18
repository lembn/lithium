import click
from calc import score_battery
import numpy as np
import matplotlib.pyplot as plt
from data.model import Model


@click.command()
@click.argument("modelpaths", nargs=-1, type=click.Path(exists=True))
def compare(modelpaths: tuple[str]):
    """Compare the models specified by MODELPATHS"""

    for modelpath in modelpaths:
        model = Model.load(modelpath)
        X = np.arange(0, 12, 0.1)
        y = np.array([score_battery(x, model) for x in X])
        plt.plot(X, y)

    ax = plt.axes()
    ax.set_xlabel("Capacity (Ah)")
    ax.set_ylabel("Flight Time (mins)")
