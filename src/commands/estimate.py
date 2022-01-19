from console import info
import click
from scraper import scrape
import numpy as np
from sklearn.linear_model import LinearRegression


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
    default="co.uk",
    help="Domain to search on if choice is available (eg. com, co.uk, ca).",
    type=click.STRING,
    show_default=True,
)
@click.option(
    "-p",
    "--pages",
    default=-1,
    help="The number of product pages to take data from per site. Set to -1 to extract data from all pages",
    type=click.INT,
    show_default=True,
)
@click.option(
    "--compound",
    default="lipo",
    help="The chemical compound of the battery",
    type=click.Choice(["lipo", "li-ion"]),
    show_default=True,
)
@click.command(short_help="Estimate a multiplier used for generating models")
def estimate(cells: int, domain: str, pages: int, compound: str):
    """Extract data of existing batteries from online e-tailers to estimate
    the relationship between capacity and mass. This estimate results is the multiplier used when generating models"""
    count, data_gen = scrape(cells, domain, pages, compound)
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
