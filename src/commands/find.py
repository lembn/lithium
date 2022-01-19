import click


@click.option(
    "-d",
    "--domain",
    prompt=True,
    help="Domain to search on if choice is available (eg. com, co.uk, ca).",
    type=click.STRING,
)
@click.command(short_help="Recommend Lithium Polymer batteries")
def find():
    """Recommend Lithium Polymer batteries sold by online e-tailers that will work well
    with a given model"""
    # TODO: recommend batteries for model
    # TODO: consider price in recommendation (user inputs price range?)
    pass
