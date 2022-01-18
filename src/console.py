import click
from datetime import datetime


def time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def info(message: str) -> None:
    click.echo(
        click.style(
            f"INFO [{time()}]: {message}",
            blink=True,
            bold=True,
            fg="green",
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
