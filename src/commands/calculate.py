import click
from console import info
from data.model import Model


@click.argument(
    "modelpath",
    type=click.STRING,
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
@click.command(short_help="Estimate the flight time of the drone from it's model")
def calculate(modelpath, capacity, mass, m, p, i, c, pm, im, b, d):
    """Calculate an estimate for the flight time of drone using it's flight time model

    MODELPATH - the relative file path of the model.json file to test aganst
    """

    model = Model.load(modelpath)
    info(f"\n RESULT: {model.model_battery(capacity, mass)} minutes")
