from datetime import datetime
import click
import matplotlib.pyplot as plt
from battery import Battery


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


def report(practical_best: list[Battery], theoretical_best: list[Battery]) -> None:
    pass


def graph(x: list[int], x_label: str, y: list[int], y_label: str) -> None:
    plt.scatter(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
