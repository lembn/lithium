import click
import commands


@click.command()
@click.group(
    help="""
    `lithium` produces models of flight times for drones from the mass and capacity of the drone's battery.
    These models can be compared to measure the flight time performance of a drone, or tested against to estimate
    flight time for a drone with a given battery. `lithium` assumes a nominal cell voltage of 3.7v
    """
)
def cli():
    pass


if __name__ == "__main__":
    cli(prog_name="lithium")
    cli.add_command(commands.estimate)
    cli.add_command(commands.generate)
    cli.add_command(commands.graph)
    cli.add_command(commands.find)
    cli.add_command(commands.calculate)
    cli.add_command(commands.compare)
