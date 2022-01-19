import click


@click.option(
    "-d",
    "--domain",
    default="co.uk",
    help="Domain to search on if choice is available (eg. com, co.uk, ca).",
    type=click.STRING,
    show_default=True,
)
@click.command(short_help="Recommend Lithium Polymer batteries")
def find():
    """Recommend Lithium Polymer batteries sold by online e-tailers that will work well
    with a given model"""
    # TODO: recommend batteries for model
    # TODO: consider price in recommendation (user inputs price range?)
    pass
