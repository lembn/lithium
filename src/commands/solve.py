import click
from model import Model
from output import msg


@click.command(short_help="Find the optimal battery for a drone")
@click.argument("modelfile", type=click.File(mode="r"))
@click.option(
    "-f",
    "--f-target",
    help="Target flight intensity",
    default=Model.F_MAX,
    show_default=True,
    type=click.FLOAT,
)
@click.option(
    "--override",
    help="Allow flight intensities above the default threshold",
    is_flag=True,
    type=click.BOOL,
    show_default=True,
)
def solve(modelfile: click.File, f_target: float, override: bool):
    """Find the optimal battery for a drone in terms of the mass and capacity of the battery
    MOTORS is the number of motors on the drone
    MASS is the mass of the drone [not including the battery]
    """

    model = Model.load(modelfile.read())
    capacity, mass, f = model.solve(f_target, override)
    msg(f"{capacity}Ah, {mass}kg @ F={f}")
