from datetime import datetime
import click
import matplotlib.pyplot as plt
from data.battery import Battery


def time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def info(message: str) -> None:
    click.echo(
        click.style(
            f"INFO [{time()}]: {message}",
            blink=True,
            bold=True,
            fg="white",
        )
    )


def warn(message: str) -> None:
    click.echo(
        click.style(
            f"WARNING [{time()}]: {message}",
            blink=True,
            bold=True,
            fg="yellow",
        )
    )


def graph(
    x: list[int], x_label: str, y: list[int], y_label: str, z: list[int], z_label: str
) -> None:
    ax = plt.axes()
    ax.scatter(x, y)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()
