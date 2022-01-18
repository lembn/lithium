import click
from scraper import scrape


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
    data = scrape(cells, domain, pages)
    # TODO: finish
    pass
