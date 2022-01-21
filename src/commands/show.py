import random
import click
import matplotlib.pyplot as plt
from model import Model
import output


@click.command()
@click.argument("modelfiles", nargs=-1, type=click.File(mode="r"))
def show(modelfiles: tuple[click.File]):
    """Show the graphs of one to six models specified by MODELFILES"""

    axs = output.get_axs()
    colours = ["#EE6666", "#3388BB", "#9988DD", "#EECC55", "#88BB44", "#FFBBBB"]

    for modelfile in modelfiles:
        model = Model.load(modelfile.read())
        x, y, _ = model.points()
        colour = random.choice(colours)
        colours.remove(colour)
        axs[0].plot(x, y, colour, label=model.name)  # TODO cycle colours
        x, y, _ = model.points(plot_f=True)
        axs[1].plot(x, y, colour, label=model.name)  # TODO cycle colours

    axs[0].legend()
    axs[1].legend()
    plt.show()
