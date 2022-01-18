from console import info
import click
from scraper import scrape
import numpy as np
from sklearn.linear_model import LinearRegression


@click.command()
@click.option(
    "-c",
    "--cells",
    prompt=True,
    help="Number of serial cells in the battery (S number).",
    type=click.INT,
)
@click.option(
    "-d",
    "--domain",
    prompt=True,
    help="Domain to search on if choice is available (eg. com, co.uk, ca).",
    type=click.STRING,
)
@click.option(
    "-p",
    "--pages",
    default=-1,
    help="The number of product pages to take data from per site. Set to -1 to extract data from all pages",
    type=click.INT,
)
def estimate(cells: int, domain: str, pages: int):
    """Extract data of existing Lithium Polymer batteries from online e-tailers to estimate
    the relationship between capacity and mass. This estimate results is the multiplier used when generating models"""
    count, data_gen = scrape(cells, domain, pages)
    capacities = []
    masses = []

    fill_char = click.style("#", fg="green")
    empty_char = click.style("-", fg="white", dim=True)
    with click.progressbar(
        data_gen,
        length=count,
        label="Collecting data...",
        fill_char=fill_char,
        empty_char=empty_char,
        show_percent=True,
        show_pos=True,
        show_eta=True,
    ) as items:
        for item in items:
            capacities.append(item.capacity)
            masses.append(item.mass)

    model = LinearRegression().fit(np.array(capacities), np.array(masses))
    info(f"Multiplier estimation: {model.coef_[0]}")
