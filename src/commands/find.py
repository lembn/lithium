import click


@click.command()
@click.option(
    "-d",
    "--domain",
    prompt=True,
    help="Domain to search on if choice is available (eg. com, co.uk, ca).",
    type=click.STRING,
)
def find():
    """Recommend Lithium Polymer batteries sold by online e-tailers that will work well
    with a given model"""
    # TODO: recommend batteries for model
    # TODO: consider price in recommendation (user inputs price range?)
    pass
