import click
import output
from model import Model

## Graphing options
@click.option(
    "--transparent",
    help="Give the graph image a transparent background",
    is_flag=True,
    type=click.BOOL,
    show_default=True,
)
@click.option(
    "--format",
    default="png",
    help="File format of the graph image",
    type=click.Choice(["png", "pdf", "svg"], case_sensitive=False),
    show_default=True,
)
@click.option(
    "--dpi", default=100, help="DPI of graph iamge", type=click.FLOAT, show_default=True
)
## Optional options
@click.option(
    "-o",
    "--outfile",
    default="./",
    help="The relative path of the directory to save the model data to.",
    type=click.Path(),
    metavar="<outfile>",
    show_default=True,
)
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
    "--compound",
    default=Model.compounds[0],
    help="The chemical compound of the battery.",
    type=click.Choice(Model.compounds),
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
    "--bias",
    default=0,
    help="Flight Intensity bias.",
    type=click.INT,
    show_default=True,
)
## Mandatory options
@click.option(
    "-v",
    "--voltage",
    prompt=True,
    help="Voltage of the battery (V).",
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
    "-m",
    "--mass",
    prompt=True,
    help="Base mass of the drone [not including battery] (kg).",
    type=click.FLOAT,
)
@click.option(
    "-n",
    "--name",
    prompt=True,
    help="Name of the model.",
    type=click.STRING,
)
@click.command(short_help="Generate a model and save it's data to <outfile>")
def generate(
    name: str,
    mass: float,
    pull: float,
    constant_current: float,
    voltage: float,
    outfile: str,
    p_max: float,
    i_max: float,
    bias: int,
    discharge: float,
    compound: str,
    dpi: float,
    format: str,
    transparent: bool,
) -> None:
    """Generate a model and save it's data to <outfile>"""

    if not p_max and not i_max:
        output.msg(
            "either p-max or i-max (or both) must be defined.", "WARNING", "yellow"
        )
        return
    output.msg("Generating...")
    outfile = outfile.strip()
    model = Model(
        name,
        mass,
        pull,
        constant_current,
        voltage,
        bias,
        discharge,
        compound,
        p_max=p_max,
        i_max=i_max,
    )
    model.save(outfile, dpi, format, transparent)
    output.msg(f"Saved to {outfile}", colour="green")
