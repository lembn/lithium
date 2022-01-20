import click
from console import info
from data.model import Model


@click.argument(
    "modelfile",
    type=click.File(mode="r"),
)
@click.argument(
    "capacity",
    type=click.FLOAT,
)
@click.argument(
    "mass",
    type=click.FLOAT,
)
@click.command(short_help="Estimate for the flight time.")
def calculate(modelfile, capacity, mass):
    """Calculate an estimate for the flight time of drone using it's flight time model.

    \b
    MODELFILE - the relative file path of the model.json file to test aganst.
    CAPACITY - The capacity of the battery (Ah).
    MASS - The mass of the battery (kg).
    """

    model = Model.load(modelfile.read())
    info(f"\n RESULT: {model.model(capacity, mass=mass)} minutes")
