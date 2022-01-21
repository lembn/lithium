import click
from datetime import datetime

from matplotlib import pyplot as plt
import matplotlib


def time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def msg(message: str, type: str = "INFO", colour: str = "white") -> None:
    click.echo(
        click.style(
            f"{type} [{time()}]: {message}",
            blink=True,
            bold=True,
            fg=colour,
        )
    )


def get_axs() -> list[matplotlib.axes]:
    plt.rc(
        "axes",
        facecolor="#E6E6E6",
        axisbelow=True,
        grid=True,
    )
    plt.rc("grid", color="w", linestyle="solid")
    plt.rc("xtick", direction="out", color="gray")
    plt.rc("ytick", direction="out", color="gray")
    plt.rc("patch", edgecolor="#E6E6E6")
    plt.rc("lines", linewidth=2)
    fig = plt.figure()
    gs = fig.add_gridspec(2, hspace=0.05, height_ratios=[3, 1])
    axs = gs.subplots(sharex=True)
    fig.suptitle("Flight Time Model")
    return axs
