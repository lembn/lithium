import console
import click
from data.model import Model

## Mandatory options
@click.option(
    "-m",
    "--mass",
    prompt=True,
    help="Base mass of the drone [not including battery] (kg).",
    type=click.FLOAT,
)
@click.option(
    "-p",
    "--pull",
    prompt=True,
    help="The pull produced by a single motor (kg).",
    type=click.FLOAT,
)
@click.option(
    "-i",
    "--constant-current",
    prompt=True,
    help="Total constant current draw of components (A).",
    type=click.FLOAT,
)
@click.option(
    "-v",
    "--voltage",
    prompt=True,
    help="Voltage of the battery (V).",
    type=click.FLOAT,
)
@click.option(
    "-o",
    "--output",
    prompt=True,
    help="The relative folder path to save the model data to.",
    type=click.STRING,
    metavar="<output>",
)
## Optional options
@click.option(
    "--p-max",
    default=0,
    help="Maximum power consumption of a single motor (W).",
    type=click.FLOAT,
    show_default=True,
)
@click.option(
    "--i-max",
    default=0,
    help="Maximum current drawn by a single motor (A).",
    type=click.FLOAT,
    show_default=True,
)
## Advanced options
@click.option(
    "--bias",
    default=0,
    help="Flight Intensity bias.",
    type=click.INT,
    show_default=True,
)
@click.option(
    "--discharge",
    default=0.8,
    help="Discharge percentage of the battery (decimal form).",
    type=click.FLOAT,
    show_default=True,
)
@click.option(
    "--multiplier",
    default=0.072,  # TODO: get better default value
    help="Value to multiply the battery capacity by to estimate mass.",
    type=click.FLOAT,
    show_default=True,
)
## Graphing options
@click.option(
    "--dpi", default=100, help="DPI of graph iamge", type=click.FLOAT, show_default=True
)
@click.option(
    "--format",
    default="png",
    help="File format of the graph image",
    type=click.Choice(["png", "pdf", "svg"], case_sensitive=False),
    show_default=True,
)
@click.option(
    "--transparent",
    help="A flag to represent if the graph image should have a transparent background",
    is_flag=True,
    type=click.BOOL,
    show_default=True,
)
@click.command(short_help="Generate a model and save it's data to <output>")
def generate(
    mass: float,
    pull: float,
    constant_current: float,
    voltage: float,
    output: str,
    p_max: float,
    i_max: float,
    bias: int,
    discharge: float,
    multiplier: float,
    dpi: float,
    format: str,
    transparent: bool,
) -> None:
    """Generate a model and save it's data to <output>"""

    if not p_max and not i_max:
        console.warn("either p-max or i-max (or both) must be defined.")
        return

    model = Model(
        mass, pull, constant_current, voltage, p_max, i_max, bias, discharge, multiplier
    )
    model.save(output, dpi, format, transparent)
    console.info(f"Saved to {output}")
