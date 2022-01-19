import click
import numpy as np
import matplotlib.pyplot as plt
from data.model import Model


@click.argument("modelpaths", nargs=-1, type=click.Path(exists=True))
@click.command(short_help="Compare the graphs of models")
def compare(modelpaths: tuple[str]):
    """Compare the models specified by MODELPATHS"""

    for modelpath in modelpaths:
        model = Model.load(modelpath)
        X = np.arange(0, 12, 0.1)
        y = np.array([model.model_capacity(x) for x in X])
        plt.plot(X, y)

    ax = plt.axes()
    ax.set_xlabel("Capacity (Ah)")
    ax.set_ylabel("Flight Time (mins)")
    plt.show()
