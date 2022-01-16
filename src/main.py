import loader
import click
from battery import Battery
from learner import predict
import output
from scraper import scrape


@click.command()
@click.option(
    "-m", "--mass", prompt=True, help="Total mass of the drone (kg).", type=click.FLOAT
)
@click.option(
    "-g",
    "--grav",
    default=9.81,
    help="Gravitational feild strength (N/kg).",
    type=click.FLOAT,
)
@click.option(
    "-n", "--motors", prompt=True, help="Number of motors on the drone.", type=click.INT
)
@click.option(
    "-t",
    "--thrust",
    prompt=True,
    help="Maximum thrust produced by a single motor (N).",
    type=click.FLOAT,
)
@click.option("-b", "--bias", default=0, help="Flight Intensity bias.", type=click.INT)
@click.option(
    "-d",
    "--domain",
    prompt=True,
    help="Domain to search on if choice is available (eg. com, co.uk, ca).",
    type=click.STRING,
)
@click.option(
    "-i",
    "--constant-current",
    prompt=True,
    help="Total constant current draw of components (A).",
    type=click.FLOAT,
)
@click.option(
    "-c",
    "--cells",
    prompt=True,
    help="Number of serial cells in the battery (S number).",
    type=click.INT,
)
@click.option(
    "--p-max",
    default=None,
    help="Maximum power consumption of a single motor (W).",
    type=click.FLOAT,
)
@click.option(
    "--i-max",
    default=None,
    help="Maximum current drawn by a single motor (A).",
    type=click.FLOAT,
)
@click.option(
    "--discharge",
    default=0.8,
    help="Discharge percentage of the battery (decimal form).",
    type=click.FLOAT,
)
def cli(
    mass: float,
    grav: float,
    motors: int,
    thrust: float,
    bias: int,
    domain: str,
    constant_current: float,
    cells: int,
    p_max: float,
    i_max: float,
    discharge: float,
) -> None:
    """
    `lithium` is a battery capacity optimiser for drone builds that uses statistical analysis and
    machine learning techniques to find the optimum battery capacity for a drone.
    """

    if not p_max and not i_max:
        output.warn("either p-max or i-max (or both) must be defined.")
        return

    batteries = scrape(cells, domain, 1)
    capacities = []
    masses = []
    practical_best = [Battery.empty()]
    for battery in batteries:
        capacities.append(battery.capacity)
        masses.append(battery.mass)
        # battery.score = score(battery)
        # data_points.append([battery.mass, battery.capacity, battery.score])
        # if battery.score > practical_best[0].score:
        #     practical_best = [battery]
        # elif battery.score == practical_best[0].score:
        #     practical_best.append(battery)

    theoretical_best = predict(data_points)

    output.report(practical_best, theoretical_best)


if __name__ == "__main__":
    output.info("Initialising...")
    capacities = []
    masses = []
    batteries = loader.load()
    if not batteries:
        batteries = scrape(3, "co.uk", 1)
        loader.open_save()
        output.info("Collecting data...")
    for battery in batteries:
        capacities.append(battery.capacity)
        masses.append(battery.mass)
        if loader.saving:
            print(battery)
            loader.save(battery)
    loader.close()
    output.graph(capacities, "Capacity", masses, "Mass")
    # cli(prog_name="lithium")
