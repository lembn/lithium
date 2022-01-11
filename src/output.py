from typing import List
import click

from battery import Battery


def warn(message: str):
    click.echo(
        click.style(
            f"WARNING: {message}",
            blink=True,
            bold=True,
            fg="yellow",
        )
    )


def report(practical_best: List[Battery], theoretical_best: List[Battery]) -> None:
    pass
