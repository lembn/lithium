from distutils.log import info
from calc import score_battery
import click
from data.model import Model


def use_model(force_options):
    #TODO: organise options in help menu
    model_options = [
        ## Mandatory options
        click.option(
            "-m",
            "--mass",
            prompt=force_options,
            help="Base mass of the drone [not including battery] (kg).",
            type=click.FLOAT,
        ),
        click.option(
            "-p",
            "--pull",
            prompt=force_options,
            help="The pull produced by a single motor (kg).",
            type=click.FLOAT,
        ),
        click.option(
            "-i",
            "--constant-current",
            prompt=force_options,
            help="Total constant current draw of components (A).",
            type=click.FLOAT,
        ),
        click.option(
            "-c",
            "--cells",
            prompt=force_options,
            help="Number of serial cells in the battery (S number).",
            type=click.INT,
        ),
        click.option(
            "--p-max",
            default=0,
            help="Maximum power consumption of a single motor (W).",
            type=click.FLOAT,
        ),
        click.option(
            "--i-max",
            default=0,
            help="Maximum current drawn by a single motor (A).",
            type=click.FLOAT,
        ),
        click.option("--bias", default=0, help="Flight Intensity bias.", type=click.INT),
        click.option(
            "--discharge",
            default=0.8,
            help="Discharge percentage of the battery (decimal form).",
            type=click.FLOAT,
        )
    ]

    def wrapper(wrapped):
        for option in reversed(model_options):
            wrapped = option(wrapped)
        return wrapped
    return wrapper

@click.command()
@click.group(
    help="""
    `lithium` produces models of flight times for drones from the mass and capacity of the drone's battery.
    These models can be compared to measure the flight time performance of a drone, or tested against to estimate
    flight time for a drone with a given battery.
    """
)
def cli():
    pass

# TODO: allow user to specify more about how model.png looks - include savefig settings
@click.option(
    "-o",
    "--output",
    prompt=True,
    help="The relative folder path to save the model data to.",
    type=click.STRING,
)
@click.option(
    "--multiplier",
    default=0.072,  # TODO: get better default value
    help="Value to multiply the battery capacity by to estimate mass.",
    type=click.FLOAT,
)
@use_model(force_options=True)
@cli.command()
def generate(
    mass: float,
    pull: float,
    constant_current: float,
    cells: int,
    output: str,
    p_max: float,
    i_max: float,
    bias: int,
    discharge: float,
    multiplier: float,
) -> None:
    """Generate a model and save it's data to OUTPUT"""

    if not p_max and not i_max:
        output.warn("either p-max or i-max (or both) must be defined.")
        return

    model = Model(
        mass, pull, constant_current, cells, p_max, i_max, bias, discharge, multiplier
    )
    model.save(output)


# TODO: allow model opts to be passed to test which will test the battery with the altered values
@click.argument(
    "modelpath",
    type=click.STRING,
)
@click.option(
    "-bc",
    "--battery-capacity",
    prompt=True,
    help="The capacity of the battery (Ah).",
    type=click.FLOAT,
)
@click.option(
    "-bm",
    "--battery-mass",
    prompt=True,
    help="The mass of the battery (kg).",
    type=click.FLOAT,
)
@use_model(force_options=False)
@cli.command()
def calculate(modelpath, battery_capacity, battery_mass, mass, pull, constant_current, cells, p_max, i_max, bias, discharge):
    """Calculate an estimate for the flight time of drone using it's flight time model

    MODEL - the relative file path of the model.json file to test aganst
    """

    model = Model.load(modelpath)
    #TODO: implement
    model.adjust(mass, pull, constant_current, cells, p_max, i_max, bias, discharge)
    info(f"\n RESULT: {score_battery(battery_capacity, battery_mass, model)} minutes")



@cli.command()
def compare():
    """Compare multiple models and their features to see which ones are stronger and why"""
    # TODO: implement model comparison
    # TODO: load multiple models onto single graph
    # TODO: load unlimited amount of models can be compared
    # TODO  recommend how to improve model
    pass


@cli.command()
def find():
    """Recommend Lithium Polymer batteries sold by online e-tailers that will work well
    with a given model"""
    # TODO: recommend batteries for model
    # TODO: consider price in recommendation (user inputs price range?)
    pass


@cli.command()
def estimate():
    """Use data of existing Lithium Polymer batteries to estimate a more accurate value
    for the multiplier used when generating models"""
    # TODO: scrape amazon to get an estimate for the multiplier
    pass

# TODO: scraper methods will requires the --domain option
# @click.option(
#     "-d",
#     "--domain",
#     default=True,
#     help="Domain to search on if choice is available (eg. com, co.uk, ca).",
#     type=click.STRING,
# )

if __name__ == "__main__":
    cli(prog_name="lithium")
