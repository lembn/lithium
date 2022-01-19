import click
from console import info
from data.model import Model


@click.argument(
    "modelfile",
    type=click.File(mode="r"),
)
## Main options
@click.option(
    "--capacity",
    prompt=True,
    help="The capacity of the battery (Ah).",
    type=click.FLOAT,
)
@click.option(
    "--mass",
    prompt=True,
    help="The mass of the battery (kg).",
    type=click.FLOAT,
)
@click.command()
def calculate(modelfile, capacity, mass):
    """Calculate an estimate for the flight time of drone using it's flight time model

    MODELFILE - the relative file path of the model.json file to test aganst
    """

    model = Model.load(modelfile.read())
    info(f"\n RESULT: {model.score_battery(capacity, mass)} minutes")
