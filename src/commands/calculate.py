import click
from console import info
from data.model import Model
from calc import score_battery


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
## Adjustment options
@click.option(
    "-m",
    help="Base mass of the drone [not including battery] (kg).",
    default=None,
    type=click.FLOAT,
)
@click.option(
    "-p",
    help="The pull produced by a single motor (kg).",
    default=None,
    type=click.FLOAT,
)
@click.option(
    "-i",
    help="Total constant current draw of components (A).",
    default=None,
    type=click.FLOAT,
)
@click.option(
    "-c",
    help="Number of serial cells in the battery (S number).",
    default=None,
    type=click.INT,
)
@click.option(
    "-o",
    help="The relative folder path to save the model data to.",
    default=None,
    type=click.STRING,
)
@click.option(
    "-pm",
    help="Maximum power consumption of a single motor (W).",
    default=None,
    type=click.FLOAT,
)
@click.option(
    "-im",
    help="Maximum current drawn by a single motor (A).",
    default=None,
    type=click.FLOAT,
)
## Advanced options
@click.option("-b", help="Flight Intensity bias.", type=click.INT)
@click.option(
    "-d",
    help="Discharge percentage of the battery (decimal form).",
    type=click.FLOAT,
)
@click.command()
def calculate(modelpath, capacity, mass, m, p, i, c, pm, im, b, d):
    """Calculate an estimate for the flight time of drone using it's flight time model

    MODEL - the relative file path of the model.json file to test aganst
    """

    model = Model.load(modelpath)
    model.adjust(m, p, i, c, pm, im, b, d)
    info(f"\n RESULT: {score_battery(capacity, mass, model)} minutes")
